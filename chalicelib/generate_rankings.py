from chalicelib.elo import calculate_elo
from chalicelib.const import RANKINGS_BUCKET, RANKINGS_DIR, GLOBAL_RANKINGS_FILE
from chalicelib.aws import s3
from chalicelib.tournaments import Tournaments
import json
from datetime import datetime
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import numpy as np

def save_locally(json_data, file_name):
    with open("chalicelib/data"+file_name, "w") as json_file:
        json.dump(json_data, json_file)
K_FACTOR = 50
def upload_to_s3(json_data, file_name):
    s3object = s3.Object(RANKINGS_BUCKET, file_name)

    s3object.put(
        Body=(bytes(json.dumps(json_data).encode('UTF-8')))
    )

def teams_by_elo(elo):
    return [team for _, team in sorted(elo.items(), key=lambda item: item[1].adjusted_elo(), reverse=True)]

def get_tournament_teams(tournament):
    for stage in tournament["stages"]:
        for section in stage["sections"]:
            for match in section["matches"]:
                if match["state"] == "completed":
                    for team in match["teams"]:
                        yield team["id"]

def generate_global_rankings(elo):
    rankings = list(i.json() for i in teams_by_elo(elo))
    return rankings    

def generate_tournament_rankings(tournaments, df, model):
    for tournament in tournaments.data:
        tournament_start_date = datetime.strptime(tournament["startDate"], "%Y-%m-%d")
        elo, _, _ = calculate_elo(tournaments, tournament["id"], tournament_start_date, k_factor=K_FACTOR, df=df, model=model)
        teams_sorted = teams_by_elo(elo)
        teams_in_tournament = list(get_tournament_teams(tournament))
        teams_sorted = [team for team in teams_sorted if team.id in teams_in_tournament]
        rankings = list(team.json() for team in teams_sorted)
        yield tournament["id"], rankings

def generate_rankings(tournaments):
    df = pd.read_csv("csv/sql/rolling.csv",
                    dtype= {
                        'blue_teamid': 'str',
                        'red_teamid': 'str',
                    })
    df["eventtime"] = pd.to_datetime(df["eventtime"], errors="coerce")
    df["blue_teamid"].fillna(0, inplace=True)
    df["red_teamid"].fillna(0, inplace=True)
    df["blue_teamid"] = df["blue_teamid"].astype(np.int64).astype(str)
    df["red_teamid"] = df["red_teamid"].astype(np.int64).astype(str)
    x = df[[
            "blue_avg_inhib", "red_avg_inhib",
            "blue_avg_tower", "red_avg_tower",
            "blue_avg_kills", "red_avg_kills",
            "blue_avg_win", "red_avg_win",
            "red_avg_deaths", "blue_avg_deaths",
            "blue_level", "red_level",
            "blue_cs", "red_cs",
            "blue_avg_kill", "red_avg_kill",
            # "blue_avg_shutdown_converted", "red_avg_shutdown_converted",
            # "blue_avg_shutdown_held", "red_avg_shutdown_held", "blue_avg_shutdown_collected", "red_avg_shutdown_collected",
    ]]
    y = df["winningteam"]
    gnb = GaussianNB()
    model = gnb.fit(x, y)
    elo, _, _ = calculate_elo(
        tournaments,
        k_factor=K_FACTOR,
        df = df,
        model = model,
    )
    global_rankings = generate_global_rankings(elo)
    upload_to_s3(global_rankings, GLOBAL_RANKINGS_FILE)
    for tournament_id, tounament_ranking in generate_tournament_rankings(tournaments, df, model):
        # save_locally(tounament_ranking, "%s%s.json" % (RANKINGS_DIR, tournament_id))
        print(tournament_id)
        if tounament_ranking:
            save_locally(tounament_ranking, "/%s.json" % (tournament_id))
            upload_to_s3(tounament_ranking, "%s%s.json" % (RANKINGS_DIR, tournament_id))
