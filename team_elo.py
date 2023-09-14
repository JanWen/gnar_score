# load all the team ids from the json file and initialize a dictionary with each
# teams elo set to 1000

import matplotlib.pyplot as plt
from esports import teams_data, tournaments_data
import statistics

ELO_GROWTH = 0.01

def update_elo(
    elo,
    blue_id,
    red_id,
    blue_elo,
    red_elo,
    blue_win
):
    # calculate elo
    kitty = ELO_GROWTH * (blue_elo + red_elo)
    elo[blue_id] -= ELO_GROWTH * blue_elo
    elo[red_id] -= ELO_GROWTH * red_elo

    if blue_win:
        elo[blue_id] += kitty
    else:
        elo[red_id] += kitty

def yield_games():
    for tournament in tournaments_data:
        for stage in tournament["stages"]:
            for section in stage["sections"]:
                for match in section["matches"]:
                    if match["state"] == "completed":
                        for game in match["games"]:
                            if game["state"] == "completed":
                                yield game


def calculate_elo():
    elo = {team["team_id"]:1000 for team in teams_data}
    back_test = {}

    for game in yield_games():
        blue_id = game["teams"][0]["id"]
        red_id = game["teams"][1]["id"]
        blue_win = game["teams"][0]["result"]["outcome"] == "win"
        try: # todo some chinese teams are not in the teams.json file
            blue_elo = elo[blue_id]
            red_elo = elo[red_id]
        except KeyError as e:
            continue
        
        
        # backtest_elo()
        elo_diff = round(blue_elo - red_elo)
        if elo_diff not in back_test:
            back_test[elo_diff] = {
                "total": 1,
            }
            if blue_win:
                back_test[elo_diff]["blue_wins"] = 1
            else:
                back_test[elo_diff]["blue_wins"] = 0
        else:
            back_test[elo_diff]["total"] += 1
            if blue_win:
                back_test[elo_diff]["blue_wins"] += 1
            

        update_elo(
            elo,
            blue_id,
            red_id,
            blue_elo,
            red_elo,
            blue_win
        )
        # check if blue tuple is really blue
        if game["teams"][0]["side"] != "blue":
            raise "FUCKING SHITBALL"
    
    return elo, back_test


def get_elo_cutoff(back_test, percentage):
    # get the elo score diff cut off at wich x% of games are included
    total_games = sum([i[1]["total"] for i in back_test.items()])
    cutoff = percentage * total_games
    print("total games", total_games)
    index = 1
    max_index = max(back_test.keys())
    while True:
        games_in_range = sum([i[1]["total"] for i in back_test.items() if i[0] > -1*index and i[0] < index])
        if games_in_range > cutoff or index > max_index:
            return index
        index += 1

