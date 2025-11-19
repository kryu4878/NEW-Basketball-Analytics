"""Utility functions for working with the sample NBA analytics data."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, Tuple

import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@lru_cache(maxsize=1)
def load_player_data() -> pd.DataFrame:
    """Return the cached player level data set."""
    return pd.read_csv(DATA_DIR / "players.csv")


@lru_cache(maxsize=1)
def load_game_data() -> pd.DataFrame:
    """Return the cached team game log data set."""
    games = pd.read_csv(DATA_DIR / "team_games.csv")
    games["date"] = pd.to_datetime(games["date"])
    return games


@lru_cache(maxsize=1)
def load_upcoming_games() -> pd.DataFrame:
    """Return the cached list of upcoming matchups."""
    upcoming = pd.read_csv(DATA_DIR / "upcoming_games.csv")
    upcoming["date"] = pd.to_datetime(upcoming["date"])
    return upcoming


def team_list() -> Iterable[str]:
    return sorted(load_player_data()["team"].unique())


def compute_team_summary(team: str) -> Dict[str, float]:
    """Aggregate a mix of traditional and advanced metrics for a team."""
    players = load_player_data()
    team_players = players[players["team"] == team]
    summary = {
        "PPG": team_players["points"].mean(),
        "Usage": team_players["usage_rate"].mean(),
        "Win Shares": team_players["win_shares"].sum(),
        "Avg Minutes": team_players["minutes"].mean(),
    }
    games = load_game_data()
    team_games = games[games["team"] == team]
    summary.update(
        {
            "Off Rating": team_games["offensive_rating"].mean(),
            "Def Rating": team_games["defensive_rating"].mean(),
            "Pace": team_games["pace"].mean(),
            "Rebound %": team_games["rebound_pct"].mean(),
        }
    )
    return {k: round(v, 2) for k, v in summary.items()}


def search_players(query: str) -> pd.DataFrame:
    """Return a filtered player table for the supplied search query."""
    players = load_player_data()
    if not query:
        return players
    mask = players["player"].str.contains(query, case=False, na=False)
    mask |= players["team"].str.contains(query, case=False, na=False)
    return players[mask]


def calculate_true_shooting(fg_pct: float, three_pct: float, ft_pct: float) -> float:
    return (fg_pct + three_pct + ft_pct) / 3


def player_projection(player_name: str) -> Dict[str, float]:
    """Estimate per-game production by blending season data and usage."""
    players = load_player_data()
    player_row = players[players["player"] == player_name]
    if player_row.empty:
        raise ValueError(f"Unknown player: {player_name}")
    row = player_row.iloc[0]

    usage_delta = row["usage_rate"] - players["usage_rate"].mean()
    projection_multiplier = 1 + (usage_delta / 100)
    projected_points = row["points"] * projection_multiplier
    projected_rebounds = row["rebounds"] * (row["minutes"] / players["minutes"].mean())
    projected_assists = row["assists"] * projection_multiplier
    true_shooting = calculate_true_shooting(row["fg_pct"], row["three_pct"], row["ft_pct"])

    return {
        "Projected Points": round(projected_points, 1),
        "Projected Rebounds": round(projected_rebounds, 1),
        "Projected Assists": round(projected_assists, 1),
        "True Shooting": round(true_shooting, 3),
    }


def _prepare_team_features() -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    games = load_game_data().copy()
    opponent_features = games[["team", "season", "offensive_rating", "defensive_rating"]]
    opponent_features = opponent_features.rename(
        columns={
            "team": "opponent",
            "offensive_rating": "opp_off_rating",
            "defensive_rating": "opp_def_rating",
        }
    )
    merged = games.merge(opponent_features, on=["opponent", "season"], how="left")
    merged["win"] = (merged["team_points"] > merged["opponent_points"]).astype(int)

    feature_cols = [
        "home",
        "pace",
        "offensive_rating",
        "defensive_rating",
        "rebound_pct",
        "assist_ratio",
        "opp_off_rating",
        "opp_def_rating",
    ]
    merged[feature_cols] = merged[feature_cols].fillna(merged[feature_cols].mean())

    return merged[feature_cols], merged["team_points"], merged["win"]


@lru_cache(maxsize=1)
def _train_models() -> Tuple[LinearRegression, LogisticRegression]:
    X, y_points, y_result = _prepare_team_features()
    reg_model = LinearRegression().fit(X, y_points)
    clf_model = LogisticRegression(max_iter=500).fit(X, y_result)
    return reg_model, clf_model


def project_upcoming_games() -> pd.DataFrame:
    """Return predictions for every entry in the upcoming games file."""
    reg_model, clf_model = _train_models()
    feature_cols, _, _ = _prepare_team_features()
    upcoming = load_upcoming_games().copy()

    opponent_lookup = (
        load_game_data()[["team", "season", "offensive_rating", "defensive_rating"]]
        .groupby("team")
        .mean()
        .rename(columns={
            "offensive_rating": "opp_off_rating",
            "defensive_rating": "opp_def_rating",
        })
    )

    team_lookup = (
        load_game_data()[["team", "pace", "offensive_rating", "defensive_rating", "rebound_pct", "assist_ratio"]]
        .groupby("team")
        .mean()
    )

    rows = []
    for _, matchup in upcoming.iterrows():
        team_profile = team_lookup.loc[matchup["team"]]
        opp_profile = opponent_lookup.loc[matchup["opponent"]]
        features = {
            "home": matchup["home"],
            "pace": team_profile["pace"],
            "offensive_rating": team_profile["offensive_rating"],
            "defensive_rating": team_profile["defensive_rating"],
            "rebound_pct": team_profile["rebound_pct"],
            "assist_ratio": team_profile["assist_ratio"],
            "opp_off_rating": opp_profile["opp_off_rating"],
            "opp_def_rating": opp_profile["opp_def_rating"],
        }
        feature_vector = pd.DataFrame([features])[feature_cols.columns]
        projected_points = float(reg_model.predict(feature_vector))
        win_probability = float(clf_model.predict_proba(feature_vector)[0, 1])

        rows.append(
            {
                "date": matchup["date"],
                "team": matchup["team"],
                "opponent": matchup["opponent"],
                "home": bool(matchup["home"]),
                "projected_points": round(projected_points, 1),
                "win_probability": round(win_probability, 3),
            }
        )
    return pd.DataFrame(rows)


def team_trend(team: str) -> pd.DataFrame:
    games = load_game_data()
    subset = games[games["team"] == team].sort_values("date")
    subset = subset[["date", "offensive_rating", "defensive_rating", "pace"]]
    return subset
