"""Create bundled CSVs that include every NBA team using plausible sample data."""
from __future__ import annotations

import csv
import datetime as dt
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
SEASONS = [2024, 2023, 2022, 2021]
random.seed(42)

team_profiles = {
    "ATL": {"pace": 101.4, "off": 118.2, "def": 119.3, "reb": 49.4, "ast": 21.3},
    "BOS": {"pace": 99.1, "off": 122.5, "def": 110.4, "reb": 53.2, "ast": 20.8},
    "BKN": {"pace": 98.7, "off": 113.1, "def": 114.5, "reb": 50.6, "ast": 19.9},
    "CHA": {"pace": 100.6, "off": 109.3, "def": 120.8, "reb": 47.2, "ast": 20.1},
    "CHI": {"pace": 97.5, "off": 114.4, "def": 113.8, "reb": 49.7, "ast": 20.5},
    "CLE": {"pace": 96.8, "off": 115.9, "def": 109.6, "reb": 51.4, "ast": 21.0},
    "DAL": {"pace": 100.1, "off": 120.6, "def": 114.1, "reb": 48.9, "ast": 21.7},
    "DEN": {"pace": 98.5, "off": 118.8, "def": 112.0, "reb": 52.6, "ast": 22.4},
    "DET": {"pace": 99.8, "off": 111.0, "def": 119.2, "reb": 50.1, "ast": 19.7},
    "GSW": {"pace": 101.9, "off": 119.6, "def": 115.8, "reb": 49.1, "ast": 23.1},
    "HOU": {"pace": 98.9, "off": 114.1, "def": 111.7, "reb": 52.0, "ast": 20.6},
    "IND": {"pace": 102.7, "off": 123.8, "def": 118.6, "reb": 50.3, "ast": 22.8},
    "LAC": {"pace": 97.2, "off": 118.4, "def": 112.3, "reb": 50.4, "ast": 20.0},
    "LAL": {"pace": 99.6, "off": 116.5, "def": 115.5, "reb": 50.8, "ast": 22.1},
    "MEM": {"pace": 99.4, "off": 109.7, "def": 112.7, "reb": 48.8, "ast": 20.9},
    "MIA": {"pace": 96.1, "off": 114.3, "def": 112.1, "reb": 49.5, "ast": 21.5},
    "MIL": {"pace": 100.9, "off": 120.3, "def": 114.6, "reb": 51.7, "ast": 21.9},
    "MIN": {"pace": 97.0, "off": 114.8, "def": 108.3, "reb": 52.4, "ast": 20.3},
    "NOP": {"pace": 98.4, "off": 117.9, "def": 112.0, "reb": 51.0, "ast": 20.7},
    "NYK": {"pace": 96.6, "off": 117.5, "def": 111.5, "reb": 54.1, "ast": 19.6},
    "OKC": {"pace": 100.5, "off": 120.8, "def": 111.2, "reb": 51.5, "ast": 22.3},
    "ORL": {"pace": 96.4, "off": 113.2, "def": 111.0, "reb": 52.2, "ast": 19.8},
    "PHI": {"pace": 98.2, "off": 117.9, "def": 112.7, "reb": 50.7, "ast": 21.4},
    "PHX": {"pace": 99.7, "off": 118.1, "def": 113.1, "reb": 51.1, "ast": 21.8},
    "POR": {"pace": 99.5, "off": 109.0, "def": 117.8, "reb": 49.8, "ast": 19.3},
    "SAC": {"pace": 101.0, "off": 118.7, "def": 116.1, "reb": 50.6, "ast": 23.0},
    "SAS": {"pace": 102.1, "off": 111.5, "def": 120.1, "reb": 50.0, "ast": 23.5},
    "TOR": {"pace": 99.3, "off": 113.7, "def": 115.0, "reb": 50.9, "ast": 22.5},
    "UTA": {"pace": 100.2, "off": 115.6, "def": 118.9, "reb": 52.8, "ast": 20.4},
    "WAS": {"pace": 102.8, "off": 114.1, "def": 121.0, "reb": 48.3, "ast": 22.2},
}

players = [
    ("Trae Young", "ATL", "PG", 74, 35.1, 26.4, 2.8, 10.8, 1.3, 0.1, 0.43, 0.365, 0.882, 30.5, 7.2),
    ("Dejounte Murray", "ATL", "SG", 78, 36.0, 22.5, 5.3, 6.4, 1.4, 0.3, 0.466, 0.365, 0.828, 26.8, 6.1),
    ("Jayson Tatum", "BOS", "SF", 74, 36.5, 27.1, 8.2, 4.4, 1.1, 0.7, 0.473, 0.375, 0.851, 30.8, 10.2),
    ("Jaylen Brown", "BOS", "SG", 72, 34.0, 24.0, 6.1, 3.6, 1.1, 0.5, 0.491, 0.359, 0.764, 28.1, 7.5),
    ("Mikal Bridges", "BKN", "SF", 82, 34.8, 19.6, 4.7, 3.6, 1.1, 0.6, 0.463, 0.379, 0.878, 24.2, 6.0),
    ("Cam Johnson", "BKN", "PF", 70, 29.5, 15.2, 5.3, 2.4, 0.9, 0.4, 0.468, 0.402, 0.808, 19.1, 3.4),
    ("LaMelo Ball", "CHA", "PG", 58, 34.2, 23.9, 6.0, 8.5, 1.7, 0.4, 0.439, 0.379, 0.878, 29.9, 4.1),
    ("Brandon Miller", "CHA", "SF", 79, 31.0, 17.3, 4.3, 2.4, 0.9, 0.6, 0.438, 0.374, 0.833, 22.7, 3.2),
    ("DeMar DeRozan", "CHI", "SF", 79, 36.5, 24.0, 4.3, 5.3, 1.1, 0.6, 0.48, 0.338, 0.872, 29.4, 7.6),
    ("Zach LaVine", "CHI", "SG", 45, 34.0, 21.0, 4.5, 3.8, 0.9, 0.4, 0.475, 0.377, 0.867, 27.8, 3.5),
    ("Donovan Mitchell", "CLE", "SG", 68, 35.6, 26.6, 5.1, 6.1, 1.8, 0.5, 0.477, 0.368, 0.872, 31.2, 8.0),
    ("Darius Garland", "CLE", "PG", 70, 34.1, 19.3, 2.7, 6.3, 1.2, 0.1, 0.462, 0.379, 0.865, 24.4, 5.6),
    ("Luka Doncic", "DAL", "PG", 75, 37.4, 33.9, 9.2, 9.8, 1.4, 0.5, 0.493, 0.372, 0.789, 35.4, 12.5),
    ("Kyrie Irving", "DAL", "PG", 70, 35.1, 25.6, 5.0, 5.2, 1.3, 0.5, 0.49, 0.411, 0.904, 27.9, 7.1),
    ("Nikola Jokic", "DEN", "C", 79, 34.6, 26.4, 12.4, 9.0, 1.4, 0.8, 0.58, 0.359, 0.832, 29.6, 15.5),
    ("Jamal Murray", "DEN", "PG", 65, 32.5, 22.1, 4.3, 6.7, 1.2, 0.3, 0.473, 0.405, 0.876, 27.1, 6.3),
    ("Cade Cunningham", "DET", "PG", 70, 34.7, 22.7, 4.3, 7.5, 1.0, 0.6, 0.456, 0.36, 0.87, 28.5, 4.7),
    ("Jalen Duren", "DET", "C", 72, 30.5, 14.1, 11.8, 2.2, 0.8, 1.3, 0.62, 0.0, 0.641, 19.5, 5.2),
    ("Stephen Curry", "GSW", "PG", 74, 34.2, 26.8, 4.7, 5.7, 0.8, 0.4, 0.468, 0.409, 0.923, 31.7, 9.8),
    ("Klay Thompson", "GSW", "SG", 78, 31.9, 17.9, 3.6, 2.3, 0.7, 0.5, 0.432, 0.385, 0.877, 23.1, 5.0),
    ("Alperen Sengun", "HOU", "C", 75, 32.1, 21.1, 9.7, 4.8, 1.2, 0.7, 0.544, 0.317, 0.78, 25.7, 7.3),
    ("Jalen Green", "HOU", "SG", 79, 33.0, 19.6, 4.9, 3.5, 0.8, 0.3, 0.427, 0.342, 0.789, 26.1, 4.1),
    ("Tyrese Haliburton", "IND", "PG", 70, 34.4, 20.1, 3.9, 11.2, 1.2, 0.5, 0.487, 0.394, 0.869, 25.0, 8.9),
    ("Myles Turner", "IND", "C", 77, 30.4, 17.1, 7.0, 1.3, 0.6, 2.1, 0.514, 0.357, 0.79, 21.4, 6.2),
    ("Kawhi Leonard", "LAC", "SF", 70, 34.3, 24.5, 6.3, 3.8, 1.6, 0.9, 0.524, 0.416, 0.887, 28.6, 9.4),
    ("Paul George", "LAC", "SG", 74, 34.0, 23.0, 6.0, 4.6, 1.5, 0.5, 0.47, 0.413, 0.897, 27.4, 8.3),
    ("LeBron James", "LAL", "SF", 72, 35.5, 25.2, 7.3, 8.1, 1.3, 0.6, 0.524, 0.411, 0.754, 30.1, 10.5),
    ("Anthony Davis", "LAL", "PF", 76, 35.0, 24.5, 12.6, 3.5, 1.2, 2.4, 0.553, 0.276, 0.821, 28.4, 12.7),
    ("Ja Morant", "MEM", "PG", 35, 35.2, 25.1, 5.6, 8.1, 1.0, 0.4, 0.473, 0.349, 0.82, 33.0, 2.9),
    ("Desmond Bane", "MEM", "SG", 60, 34.5, 23.7, 4.8, 5.4, 1.1, 0.4, 0.476, 0.401, 0.883, 27.6, 4.7),
    ("Jimmy Butler", "MIA", "SF", 62, 33.0, 22.9, 5.9, 5.3, 1.7, 0.4, 0.535, 0.357, 0.858, 27.1, 7.9),
    ("Bam Adebayo", "MIA", "C", 75, 35.0, 20.7, 10.4, 3.9, 1.1, 1.1, 0.553, 0.111, 0.778, 26.2, 9.1),
    ("Giannis Antetokounmpo", "MIL", "PF", 73, 35.1, 30.2, 11.5, 6.5, 1.2, 1.4, 0.611, 0.296, 0.652, 34.7, 12.0),
    ("Damian Lillard", "MIL", "PG", 73, 35.2, 27.1, 4.8, 7.2, 1.0, 0.3, 0.448, 0.371, 0.89, 30.3, 8.4),
    ("Anthony Edwards", "MIN", "SG", 79, 36.0, 26.6, 5.5, 5.1, 1.4, 0.7, 0.476, 0.367, 0.84, 29.1, 9.7),
    ("Karl-Anthony Towns", "MIN", "PF", 70, 33.2, 22.1, 8.4, 3.0, 0.7, 0.8, 0.502, 0.418, 0.874, 25.4, 7.4),
    ("Zion Williamson", "NOP", "PF", 68, 32.3, 23.0, 5.9, 5.0, 1.1, 0.6, 0.58, 0.365, 0.714, 29.9, 6.5),
    ("Brandon Ingram", "NOP", "SF", 70, 34.1, 22.3, 5.6, 5.8, 1.0, 0.7, 0.487, 0.362, 0.868, 27.4, 6.1),
    ("Jalen Brunson", "NYK", "PG", 77, 35.0, 28.4, 3.5, 6.7, 1.0, 0.2, 0.491, 0.401, 0.874, 30.8, 9.4),
    ("Julius Randle", "NYK", "PF", 65, 34.2, 24.1, 9.8, 4.5, 0.9, 0.4, 0.458, 0.336, 0.756, 28.8, 7.1),
    ("Shai Gilgeous-Alexander", "OKC", "PG", 75, 35.3, 30.1, 5.6, 6.2, 2.1, 0.7, 0.535, 0.387, 0.874, 32.0, 11.7),
    ("Chet Holmgren", "OKC", "C", 82, 31.0, 16.5, 7.9, 2.7, 0.9, 2.3, 0.537, 0.371, 0.795, 22.0, 7.0),
    ("Paolo Banchero", "ORL", "PF", 80, 34.8, 22.7, 6.9, 5.4, 1.1, 0.6, 0.451, 0.338, 0.737, 28.4, 6.9),
    ("Franz Wagner", "ORL", "SF", 78, 33.4, 19.7, 5.3, 3.8, 1.1, 0.3, 0.475, 0.358, 0.843, 24.1, 5.5),
    ("Joel Embiid", "PHI", "C", 39, 34.0, 34.1, 11.0, 5.6, 1.1, 1.7, 0.522, 0.381, 0.882, 36.3, 7.8),
    ("Tyrese Maxey", "PHI", "SG", 78, 37.5, 25.9, 3.7, 6.2, 1.0, 0.5, 0.456, 0.373, 0.862, 27.7, 8.8),
    ("Devin Booker", "PHX", "SG", 75, 35.7, 27.5, 4.7, 6.9, 1.1, 0.4, 0.49, 0.378, 0.883, 30.2, 8.9),
    ("Kevin Durant", "PHX", "SF", 78, 36.1, 29.0, 6.8, 5.2, 0.9, 1.4, 0.563, 0.422, 0.91, 32.6, 10.7),
    ("Anfernee Simons", "POR", "SG", 65, 35.3, 22.6, 3.6, 5.5, 0.8, 0.2, 0.445, 0.387, 0.877, 27.5, 4.0),
    ("Scoot Henderson", "POR", "PG", 68, 29.1, 14.6, 4.1, 6.2, 1.1, 0.3, 0.383, 0.323, 0.769, 26.4, 2.2),
    ("De'Aaron Fox", "SAC", "PG", 74, 35.4, 26.6, 4.5, 6.4, 1.8, 0.5, 0.476, 0.368, 0.761, 30.8, 8.3),
    ("Domantas Sabonis", "SAC", "C", 82, 35.7, 19.4, 13.7, 8.2, 1.1, 0.6, 0.595, 0.373, 0.74, 22.9, 10.8),
    ("Victor Wembanyama", "SAS", "C", 71, 29.5, 21.4, 10.6, 3.9, 1.2, 3.2, 0.474, 0.321, 0.794, 29.6, 6.7),
    ("Devin Vassell", "SAS", "SG", 72, 33.0, 19.5, 3.8, 4.1, 1.1, 0.6, 0.474, 0.378, 0.81, 24.7, 4.4),
    ("Scottie Barnes", "TOR", "SF", 77, 35.0, 20.1, 8.2, 6.1, 1.2, 1.5, 0.475, 0.349, 0.783, 25.3, 6.4),
    ("RJ Barrett", "TOR", "SG", 70, 34.0, 19.4, 5.3, 3.5, 0.7, 0.2, 0.479, 0.362, 0.816, 25.0, 4.1),
    ("Lauri Markkanen", "UTA", "PF", 70, 34.3, 23.2, 8.1, 2.9, 0.9, 0.5, 0.487, 0.396, 0.892, 26.6, 7.3),
    ("Collin Sexton", "UTA", "PG", 75, 30.1, 18.6, 2.9, 4.9, 0.8, 0.1, 0.497, 0.391, 0.831, 24.8, 4.0),
    ("Kyle Kuzma", "WAS", "PF", 78, 34.7, 22.2, 6.5, 4.2, 0.7, 0.6, 0.456, 0.339, 0.78, 29.2, 5.3),
    ("Jordan Poole", "WAS", "SG", 80, 31.5, 17.4, 2.7, 4.4, 1.1, 0.3, 0.411, 0.333, 0.871, 26.0, 3.1),
]


LATEST_SEASON = SEASONS[0]


def _season_multiplier(season: int) -> float:
    """Introduce small drifts so past seasons look slightly different."""

    offset = LATEST_SEASON - season
    return 1 - (offset * 0.015)


def _jitter(value: float, pct: float = 0.05) -> float:
    return value * (1 + random.uniform(-pct, pct))


def build_players():
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_DIR / "players.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "player",
                "team",
                "position",
                "season",
                "games_played",
                "minutes",
                "points",
                "rebounds",
                "assists",
                "steals",
                "blocks",
                "fg_pct",
                "three_pct",
                "ft_pct",
                "usage_rate",
                "win_shares",
            ]
        )
        for season in SEASONS:
            scale = _season_multiplier(season)
            for row in players:
                (
                    name,
                    team,
                    position,
                    games,
                    minutes_base,
                    points,
                    rebounds,
                    assists,
                    steals,
                    blocks,
                    fg_pct_base,
                    three_pct_base,
                    ft_pct_base,
                    usage_base,
                    win_shares_base,
                ) = row

                games_played = max(45, int(_jitter(games * scale, 0.03)))
                minutes = round(_jitter(minutes_base * scale, 0.04), 1)
                stat_block = [
                    round(_jitter(points * scale, 0.05), 1),
                    round(_jitter(rebounds * scale, 0.05), 1),
                    round(_jitter(assists * scale, 0.05), 1),
                    round(_jitter(steals * scale, 0.06), 1),
                    round(_jitter(blocks * scale, 0.06), 1),
                ]
                fg_pct = round(min(0.65, max(0.35, _jitter(fg_pct_base, 0.04))), 3)
                three_pct = round(min(0.5, max(0.28, _jitter(three_pct_base, 0.06))), 3)
                ft_pct = round(min(0.95, max(0.65, _jitter(ft_pct_base, 0.03))), 3)
                usage = round(min(36.0, max(16.0, _jitter(usage_base, 0.05))), 1)
                win_shares = round(_jitter(win_shares_base * scale, 0.08), 1)
                writer.writerow(
                    (
                        name,
                        team,
                        position,
                        season,
                        games_played,
                        minutes,
                        *stat_block,
                        fg_pct,
                        three_pct,
                        ft_pct,
                        usage,
                        win_shares,
                    )
                )


def build_team_games():
    rows = []
    team_list = list(team_profiles.keys())
    for season in SEASONS:
        base_date = dt.date(season, 1, 3)
        scale = _season_multiplier(season)
        for idx, team in enumerate(team_list):
            for offset in range(4):
                opponent = team_list[(idx + offset + 5) % len(team_list)]
                metrics = team_profiles[team]
                pace = round(_jitter(metrics["pace"] * scale, 0.02), 1)
                off = metrics["off"] * scale + random.uniform(-4, 4)
                def_rating = metrics["def"] * scale + random.uniform(-4, 4)
                team_points = int(off / 100 * pace * 1.02)
                opponent_points = max(90, int(team_points - random.uniform(-15, 15)))
                rows.append(
                    [
                        (base_date + dt.timedelta(days=idx + offset)).isoformat(),
                        season,
                        team,
                        opponent,
                        1 if offset % 2 == 0 else 0,
                        team_points,
                        opponent_points,
                        pace,
                        round(off, 1),
                        round(def_rating, 1),
                        round(_jitter(metrics["reb"] * scale, 0.03), 1),
                        round(_jitter(metrics["ast"] * scale, 0.03), 1),
                    ]
                )
    with open(DATA_DIR / "team_games.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "date",
                "season",
                "team",
                "opponent",
                "home",
                "team_points",
                "opponent_points",
                "pace",
                "offensive_rating",
                "defensive_rating",
                "rebound_pct",
                "assist_ratio",
            ]
        )
        writer.writerows(rows)


def build_upcoming():
    rows = []
    team_list = list(team_profiles.keys())
    base_date = dt.date.today() + dt.timedelta(days=1)
    for idx in range(0, len(team_list), 2):
        team = team_list[idx]
        opponent = team_list[(idx + 1) % len(team_list)]
        rows.append([base_date.isoformat(), team, opponent, 1])
        rows.append([base_date.isoformat(), opponent, team, 0])
    with open(DATA_DIR / "upcoming_games.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "team", "opponent", "home"])
        writer.writerows(rows)


if __name__ == "__main__":
    build_players()
    build_team_games()
    build_upcoming()
    print("Sample data written to data/*.csv")
