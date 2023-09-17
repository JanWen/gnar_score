# load all the team ids from the json file and initialize a dictionary with each
# teams elo set to 1000

import matplotlib.pyplot as plt
from src.esports import teams_data, tournaments_data
import statistics#
from src.leagues import league_points
from datetime import datetime
from src.team import Team

ELO_GROWTH = 0.01
BASE_ELO = 1000
K_FACTOR = 50


def yield_matches():
    for tournament in tournaments_data:
        # if tournament["leagueId"] != "98767991302996019":
        #     continue
        for stage in tournament["stages"]:
            for section in stage["sections"]:
                for match in section["matches"]:
                    if match["state"] == "completed":
                        yield tournament, tournament["leagueId"], match

def yield_games():
    for tournament, league_id, match in yield_matches():
        for game in match["games"]:
            if game["state"] == "completed":
                yield tournament, league_id, game


def init_elo():
    return {team["team_id"]:Team((team["team_id"],BASE_ELO)) for team in teams_data}


def rank_teams(teams_sorted):
    for i, team in enumerate(teams_sorted):
        team.rank = i + 1
        yield team

def global_rankings():
    elo, _ = calculate_elo()
    teams_sorted = [team for _, team in sorted(elo.items(), key=lambda item: item[1].elo, reverse=True)]
    return rank_teams(teams_sorted)

def team_rankings(team_ids):
    elo, _ = calculate_elo()
    teams_sorted = [team for _, team in sorted(elo.items(), key=lambda item: item[1].elo, reverse=True) if team.id in team_ids]
    return rank_teams(teams_sorted)


def get_tournament_teams(tournament):
    for stage in tournament["stages"]:
        for section in stage["sections"]:
            for match in section["matches"]:
                if match["state"] == "completed":
                    for team in match["teams"]:
                        yield team["id"]

def tournament_rankings(tournament_id):
    elo, _ = calculate_elo(tournament_id)
    teams_sorted = [team for _, team in sorted(elo.items(), key=lambda item: item[1].elo, reverse=True)]

    tournament = [tournament for tournament in tournaments_data if tournament["id"] == tournament_id][0]
    teams_in_tournament = list(get_tournament_teams(tournament))
    teams_sorted = [team for team in teams_sorted if team.id in teams_in_tournament]
    return rank_teams(teams_sorted)

def update_elo_real(
    elo,
    blue_id,
    red_id,
    blue_elo,
    red_elo,
    blue_win,
):
    expected_score_blue = 1/(1+10**((red_elo-blue_elo)/480))
    expected_score_red = 1 - expected_score_blue
    print(expected_score_blue,expected_score_red)
    if blue_win:
        elo[blue_id].elo = blue_elo + K_FACTOR*(1-expected_score_blue)
        elo[red_id].elo = red_elo + K_FACTOR*(0-expected_score_red)
    else:
        elo[blue_id].elo = blue_elo + K_FACTOR*(0-expected_score_blue)
        elo[red_id].elo = red_elo + K_FACTOR*(1-expected_score_red)


def calculate_elo(tournament_id=None, startDate=datetime.now()):
    elo = init_elo()
    back_test = {}

    for tournament, league_id, game in yield_games():
        if tournament_id and tournament["id"] != tournament_id:
            break
        tournament_start_date = datetime.strptime(tournament["startDate"], "%Y-%m-%d")
        days_since = (startDate- tournament_start_date).days
        if days_since > 365:
            continue
        blue_id = game["teams"][0]["id"]
        red_id = game["teams"][1]["id"]
        blue_win = game["teams"][0]["result"]["outcome"] == "win"
        if game["teams"][0]["side"] != "blue":
            raise "FUCKING SHITBALL"
        try: # todo some chinese teams are not in the teams.json file
            blue_elo = elo[blue_id].elo
            red_elo = elo[red_id].elo
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
            

        update_elo_real(
            elo,
            blue_id,
            red_id,
            blue_elo,
            red_elo,
            blue_win
        )
        elo[blue_id].games += 1
        elo[red_id].games += 1
        # check if blue tuple is really blue
        
    
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

