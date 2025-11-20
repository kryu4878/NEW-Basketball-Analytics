# Basketball-Analytics
Personal project where I have a dashboard to display NBA analytics and search up any sort of data and create projections

This project provides a lightweight NBA analytics lab where you can explore sample player and team data, search for specific players, and generate projections for upcoming matchups.

## Features

- Interactive Streamlit dashboard for browsing team summaries, player search results, and projected stat lines.
- Sample data sets for players, team game logs, and upcoming games that already cover **all 30 NBA teams** across the current season plus the previous three campaigns, so every franchise has historical context out of the box.
- Simple regression/classification models (built with scikit-learn) that estimate team scoring output and win probability for scheduled games.

## Getting started (first-timer friendly)

The steps below assume you have never run a Python/Streamlit project before. Follow them in order and you will end up with the dashboard open in your browser.

### 1. Install the required tools

1. **Install Python 3.9 or newer (current macOS installer is 3.12.x and newer 3.13 builds also work).**
   * Windows/macOS: download from [python.org/downloads](https://www.python.org/downloads/). During installation on Windows, check "Add Python to PATH." macOS currently shows Python 3.12.x as the latest stable build; if you see a 3.13.x universal installer, that release is fully compatible with this project as well.
   * Linux (Ubuntu/Debian): `sudo apt update && sudo apt install python3 python3-venv python3-pip`.
2. **Install Git** so you can download the project (skip if you already use GitHub Desktop, etc.).
   * Windows: install [Git for Windows](https://git-scm.com/download/win) and accept the defaults.
   * macOS: install Xcode Command Line Tools (`xcode-select --install`) or use [Homebrew](https://brew.sh/) with `brew install git`.
   * Linux: `sudo apt install git`.
3. **Install an IDE or code editor (optional but recommended).** [Visual Studio Code](https://code.visualstudio.com/) works on Windows, macOS, and Linux. Accept the defaults, then launch it once to finish the setup. See the "macOS + VS Code quickstart" section below if you want detailed Mac instructions. Prefer to skip an IDE? On macOS you can rely on the built-in **Terminal** app (Applications → Utilities → Terminal) for every command plus Finder/TextEdit (or another editor you already use) to view files—the rest of this guide works the same either way.

### 2. Download the project files

You have two options:

* **Git clone (recommended):**
  ```bash
  git clone https://github.com/<your-account>/Basketball-Analytics.git
  cd Basketball-Analytics
  ```
* **Download ZIP:** Click the green "Code" button on GitHub → "Download ZIP" → unzip it → open the folder in VS Code/File Explorer/ Finder.

### 3. Create an isolated Python environment and install dependencies

All commands below are run inside the project folder you just downloaded.

1. Create the environment:
   ```bash
   python -m venv .venv
   ```
2. Activate it:
   * **Windows (PowerShell):** `.​.venv\Scripts\Activate`
   * **Windows (Command Prompt):** `.venv\Scripts\activate`
   * **macOS/Linux:** `source .venv/bin/activate`
3. Install the required packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

> If any command fails, read the error message—missing `pip` or `venv` usually means Python was not added to PATH. Re-run the installer and ensure that option is checked (Windows) or open a new terminal after installation (macOS/Linux).

### 4. Launch the Streamlit dashboard

```bash
streamlit run app.py
```

Streamlit prints a **local URL** (for example `http://localhost:8501`). Copy/paste it into your browser. Keep the terminal window open while you use the dashboard.

Need to share the dashboard? Repeat the same steps on a machine that is publicly reachable (or deploy to Streamlit Community Cloud) and share the URL that Streamlit displays after starting.

## macOS + VS Code quickstart

Everything below assumes you want to stay inside Visual Studio Code on a Mac. Follow each bullet in order after you install Python and Git from the "Getting started" section above.

1. **Install Visual Studio Code.**
   * Download the macOS `.zip` from [code.visualstudio.com](https://code.visualstudio.com/Download).
   * Drag `Visual Studio Code.app` into `Applications`, then open it once so macOS trusts the app.
2. **Add the Python extension (version 2024.4.1 or "Python 4.1" is perfect).**
   * Click the square Extensions icon on the left (or press `Shift` + `Cmd` + `X`).
   * Search for **Python** by Microsoft, click **Install**, and let VS Code reload. The exact extension version does not matter as long as it is the official Microsoft release—"Python 4.1" is simply the current numbered build and works great. The extension automatically detects whichever Python you installed (3.9–3.13).
   * (Optional) Install **Pylance** for richer IntelliSense.
3. **Create a dedicated workspace folder.**
   * In Finder, make a parent folder such as `~/Projects/BasketballLab` so you know where everything lives.
   * Right-click that folder and choose **New Terminal at Folder** (or open Terminal and `cd` into it). This terminal is where you will run `git clone` or unzip the project.
4. **Download the project inside that folder.**
   * Use `git clone https://github.com/<your-account>/Basketball-Analytics.git` (or drop the unzipped folder) so you end up with `~/Projects/BasketballLab/Basketball-Analytics`.
5. **Open the folder in VS Code.**
   * In VS Code choose **File → Open Folder…**, select the `Basketball-Analytics` folder you just created, and click **Open**.
   * When prompted, click **Yes, I trust the authors** so VS Code can run tasks inside the workspace.
6. **Use the integrated terminal for every command.**
   * Press `` Ctrl ` `` (Control + backtick) or go to **View → Terminal**. VS Code opens a shell that automatically starts inside your project folder.
   * Run the setup commands in order:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     pip install --upgrade pip
     pip install -r requirements.txt
     streamlit run app.py
     ```
   * The blue status bar on the bottom-left shows which Python interpreter is active. It should switch to `.venv` shortly after you run `source .venv/bin/activate`; if it does not, press `Cmd` + `Shift` + `P`, type **Python: Select Interpreter**, and choose the `.venv` entry manually.
7. **Organize and explore files directly in VS Code.**
   * Use the Explorer sidebar to drag/drop files, create new folders (e.g., `data/custom/`), or duplicate CSVs. Right-click the `data` folder and choose **New File** whenever you want to add another dataset.
   * Double-click `app.py` or anything under `src/` to edit code; the Python extension automatically formats and lint-checks the files as you type.
8. **Run or debug inside VS Code.**
   * Once Streamlit is running, VS Code’s terminal will show the `http://localhost:8501` link; click it to open the dashboard.
   * To debug, open `app.py`, click **Run → Start Debugging**, choose **Python File**, and VS Code will attach to the Streamlit process so you can step through functions in `src/analytics.py`.

Following this flow keeps your downloads, terminal commands, and edits contained inside Visual Studio Code, which is ideal when you're just getting started on macOS.

### Python version FAQ

- **Is Python 3.13.9 the newest macOS release?** At the moment python.org distributes Python 3.12.x as the current stable macOS installer, while preview builds of 3.13.x are also appearing. Either option is fine—the project only requires "Python 3.9 or newer" and has been tested on 3.12, which means 3.13.x (stable or beta) runs the dashboard without changes.

## Project structure

```
├── app.py                # Streamlit dashboard entry point
├── data                  # Sample player, game log, and schedule data (all 30 teams)
├── requirements.txt      # Python dependencies
├── scripts               # Data utilities (refresh data, rebuild samples)
└── src/analytics.py      # Helper functions + projection pipeline
```

### Working with your own data

Replace any of the CSVs under `data/` with your personal exports (player tracking, game logs, etc.). As long as the columns remain the same, the dashboard will automatically surface the new information the next time you restart Streamlit.

Feel free to fork the project and extend the `src/analytics.py` helpers if you want to plug in different models or visualizations.

## Keeping the data fresh

The repository ships with curated CSVs that already include every NBA team, but you can rebuild or refresh them whenever you want.

### Quickly regenerate the bundled sample set

If you simply want to recreate the exact data that ships with the repo (for example, after experimenting with your own exports), run:

```bash
python scripts/build_sample_data.py
```

This recreates `data/players.csv`, `data/team_games.csv`, and `data/upcoming_games.csv` using the same plausible-but-fake numbers committed here. The script automatically targets the active NBA season (based on today’s date) plus the previous three seasons, so the bundled samples stay aligned with the current year whenever you rerun it.

### Pull real numbers from NBA.com

For live data, the project now includes `scripts/refresh_data.py`, which talks to the public NBA Stats endpoints through the [`nba_api`](https://github.com/swar/nba_api) client. You can either pull the active season **plus a specific number of previous seasons** or pin an **earliest season** to include all years through today (helpful if you want to cover 2021-22 up to the current campaign in one shot).

Make sure your virtual environment has the requirements installed and then run:

```bash
# Example 1: grab current season + 3 prior seasons (default behavior)
python scripts/refresh_data.py --season 2024-25 --past-seasons 3 --games-per-team 8 --days-ahead 7

# Example 2: ensure you always have 2021-22 through the active season
python scripts/refresh_data.py --season 2024-25 --since-season 2021 --games-per-team 8 --days-ahead 7
```

Arguments:

- `--season`: season string in NBA format (e.g., `2024-25`).
- `--past-seasons`: how many completed seasons to include in addition to the one above (defaults to `3`, giving you four total seasons of data). Mutually exclusive with `--since-season`.
- `--since-season`: earliest starting season to include (e.g., `2021` or `2021-22`) if you want a contiguous history up to the active season. Mutually exclusive with `--past-seasons`.
- `--games-per-team`: how many recent game logs to keep for each franchise **per season** (used for the projection models).
- `--days-ahead`: how far into the future to pull the NBA schedule for the `upcoming_games.csv` predictions.

The script saves the refreshed CSVs under `data/` so the next `streamlit run app.py` automatically uses the new numbers. NBA.com occasionally rate-limits these endpoints; if you see HTTP 429 errors, wait a few seconds and re-run the command.
