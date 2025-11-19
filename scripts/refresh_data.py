"""Download up-to-date NBA data and refresh the local CSV files.

This script relies on the public `nba_api` package, which scrapes the same
endpoints used by NBA.com.  The requests can occasionally be throttled, so if
you receive HTTP 429 errors simply wait a few seconds and retry.
"""
from __future__ import annotations

import argparse
import datetime as dt
import time
from pathlib import Path
from typing import Dict, List

import pandas as pd
from nba_api.stats.endpoints import (
    boxscoreadvancedv2,
    leaguegamelog,
    leaguedashplayerstats,
    scoreboardv2,
)
from nba_api.stats.library.parameters import Season
from nba_api.stats.static import teams as static_teams

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_SEASON = Season.current_season


def _retry(func, *args, **kwargs):
    for attempt in range(5):
        try:
            return func(*args, **kwargs)
        except Exception:  # pragma: no cover - just a lightweight retry helper
            if attempt == 4:
                raise
            time.sleep(1 + attempt)
    raise RuntimeError("unreachable")


def fetch_player_stats(season: str) -> pd.DataFrame:
    response = _retry(
        leaguedashplayerstats.LeagueDashPlayerStats,
        season=season,
        season_type_all_star="Regular Season",
        per_mode_detailed="PerGame",
    )
    df = response.get_data_frames()[0]
    df = df[
        [
            "PLAYER_NAME",
            "TEAM_ABBREVIATION",
            "PLAYER_POSITION",
            "GP",
            "MIN",
            "PTS",
            "REB",
            "AST",
            "STL",
            "BLK",
            "FG_PCT",
            "FG3_PCT",
            "FT_PCT",
            "USG_PCT",
            "W_PCT",
        ]
    ].rename(
        columns={
            "PLAYER_NAME": "player",
            "TEAM_ABBREVIATION": "team",
            "PLAYER_POSITION": "position",
            "GP": "games_played",
            "MIN": "minutes",
            "PTS": "points",
            "REB": "rebounds",
            "AST": "assists",
            "STL": "steals",
            "BLK": "blocks",
            "FG_PCT": "fg_pct",
            "FG3_PCT": "three_pct",
            "FT_PCT": "ft_pct",
            "USG_PCT": "usage_rate",
        }
    )
    df["season"] = season.split("-")[0]
    df["win_shares"] = (df["games_played"] * df["W_PCT"]).round(1)
    return df.drop(columns=["W_PCT"])


def _team_lookup() -> Dict[int, str]:
    return {team["id"]: team["abbreviation"] for team in static_teams.get_teams()}


def _parse_opponent(matchup: str) -> str:
    # Example formats: "BOS vs. MIA", "LAL @ DEN"
    parts = matchup.replace(".", "").split(" ")
    return parts[-1]


def fetch_team_games(season: str, games_per_team: int) -> pd.DataFrame:
    log = _retry(
        leaguegamelog.LeagueGameLog,
        season=season,
        season_type_all_star="Regular Season",
        player_or_team_abbreviation="T",
    ).get_data_frames()[0]

    log["GAME_DATE"] = pd.to_datetime(log["GAME_DATE"])
    log.sort_values(["TEAM_ABBREVIATION", "GAME_DATE"], ascending=[True, False], inplace=True)

    advanced_cache: Dict[str, pd.DataFrame] = {}
    rows = []

    for team, group in log.groupby("TEAM_ABBREVIATION"):
        subset = group.head(games_per_team)
        for _, game in subset.iterrows():
            game_id = game["GAME_ID"]
            if game_id not in advanced_cache:
                advanced_cache[game_id] = _retry(boxscoreadvancedv2.BoxScoreAdvancedV2, game_id=game_id).get_data_frames()[0]
            advanced_row = advanced_cache[game_id]
            advanced_team = advanced_row[advanced_row["TEAM_ABBREVIATION"] == team].iloc[0]

            opponent = _parse_opponent(game["MATCHUP"])
            home = 1 if "vs" in game["MATCHUP"].lower() else 0
            opponent_points = int(game["PTS"] - game["PLUS_MINUS"])

            rows.append(
                {
                    "date": game["GAME_DATE"].date().isoformat(),
                    "season": season.split("-")[0],
                    "team": team,
                    "opponent": opponent,
                    "home": home,
                    "team_points": int(game["PTS"]),
                    "opponent_points": opponent_points,
                    "pace": float(advanced_team["PACE"]),
                    "offensive_rating": float(advanced_team["OFF_RATING"]),
                    "defensive_rating": float(advanced_team["DEF_RATING"]),
                    "rebound_pct": float(advanced_team["REB_PCT"]),
                    "assist_ratio": float(advanced_team["AST_RATIO"]),
                }
            )
    games = pd.DataFrame(rows)
    return games.sort_values("date")


def fetch_upcoming_games(days_ahead: int) -> pd.DataFrame:
    team_map = _team_lookup()
    today = dt.date.today()
    rows = []
    for offset in range(days_ahead):
        game_date = today + dt.timedelta(days=offset)
        response = _retry(scoreboardv2.ScoreboardV2, game_date=game_date.strftime("%m/%d/%Y"))
        games = response.game_header.get_data_frame()
        if games.empty:
            continue
        for _, game in games.iterrows():
            home_team = team_map.get(game["HOME_TEAM_ID"])
            away_team = team_map.get(game["VISITOR_TEAM_ID"])
            if not home_team or not away_team:
                continue
            rows.append(
                {
                    "date": pd.to_datetime(game["GAME_DATE_EST"]).date().isoformat(),
                    "team": home_team,
                    "opponent": away_team,
                    "home": 1,
                }
            )
            rows.append(
                {
                    "date": pd.to_datetime(game["GAME_DATE_EST"]).date().isoformat(),
                    "team": away_team,
                    "opponent": home_team,
                    "home": 0,
                }
            )
    if not rows:
        raise RuntimeError("No scheduled games were returned by the NBA API.")
    return pd.DataFrame(rows).drop_duplicates()


def _season_string(start_year: int) -> str:
    return f"{start_year}-{str(start_year + 1)[-2:]}"


def determine_recent_seasons(latest_season: str, past_seasons: int) -> List[str]:
    """Return NBA-formatted strings for the current season plus prior seasons."""

    start_year = int(latest_season.split("-")[0])
    return [_season_string(start_year - offset) for offset in range(past_seasons + 1)]


def refresh(season: str, past_seasons: int, games_per_team: int, days_ahead: int) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    seasons = determine_recent_seasons(season, past_seasons)

    player_frames: List[pd.DataFrame] = []
    for season_str in seasons:
        print(f"Fetching player stats for {season_str}...")
        player_frames.append(fetch_player_stats(season_str))
    players = pd.concat(player_frames, ignore_index=True)
    players.to_csv(DATA_DIR / "players.csv", index=False)
    print(f"Saved {len(players)} player rows across {len(seasons)} seasons")

    team_frames: List[pd.DataFrame] = []
    for season_str in seasons:
        print(f"Fetching {games_per_team} recent games for every team in {season_str}...")
        team_frames.append(fetch_team_games(season_str, games_per_team))
    team_games = pd.concat(team_frames, ignore_index=True)
    team_games.to_csv(DATA_DIR / "team_games.csv", index=False)
    print(f"Saved {len(team_games)} team game rows across {len(seasons)} seasons")

    print(f"Fetching scheduled games for next {days_ahead} days...")
    upcoming = fetch_upcoming_games(days_ahead)
    upcoming.to_csv(DATA_DIR / "upcoming_games.csv", index=False)
    print(f"Saved {len(upcoming)} upcoming matchups")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--season", default=DEFAULT_SEASON, help="Season string such as 2024-25")
    parser.add_argument(
        "--past-seasons",
        type=int,
        default=3,
        help="How many completed seasons to include in addition to the one provided",
    )
    parser.add_argument(
        "--games-per-team", type=int, default=6, help="Number of recent games to include per team per season"
    )
    parser.add_argument("--days-ahead", type=int, default=5, help="How many days ahead to pull schedule data")
    args = parser.parse_args()
    refresh(args.season, args.past_seasons, args.games_per_team, args.days_ahead)
