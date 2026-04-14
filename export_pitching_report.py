import json
import os
from datetime import date, timedelta
from gamescore_calc import get_daily_pitcher_stats, calc_gamescore

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "pitching_report.json")

def export_report(game_date=None):
    if game_date is None:
        game_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    pitchers = get_daily_pitcher_stats(game_date)
    pitchers = calc_gamescore(pitchers)
    pitchers = pitchers.sort_values("GameScore", ascending=False).reset_index(drop=True)

    columns = ["Pitcher", "Team", "Innings", "SO", "H", "ER", "UER", "BB", "GameScore"]
    records = pitchers[columns].to_dict(orient="records")

    output = {
        "date": game_date,
        "pitchers": records,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Exported {len(records)} pitchers for {game_date} → {OUTPUT_PATH}")

if __name__ == "__main__":
    export_report()
