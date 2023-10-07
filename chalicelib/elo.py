# load all the team ids from the json file and initialize a dictionary with each
# teams elo set to 1000

from chalicelib.esports import teams_data, yield_games
from chalicelib.leagues import league_points
from datetime import datetime
from chalicelib.team import Team

ELO_GROWTH = 0.01
BASE_ELO = 1000
K_FACTOR = 50

# class Elo():
#     def __init__(self) -> None:
#         self.elo = {team["team_id"]:Team((team["team_id"],BASE_ELO)) for team in teams_data}

#     def yield_games():


#     def update_elo(self, tournament):


def init_elo():
    return {team["team_id"]:Team((team["team_id"],BASE_ELO)) for team in teams_data}

def update_elo(
    elo,
    blue_id,
    red_id,
    blue_elo,
    red_elo,
    blue_win,
    k_factor = K_FACTOR
):
    if not k_factor:
        k_factor = K_FACTOR
    expected_score_blue = 1/(1+10**((red_elo-blue_elo)/480))
    expected_score_red = 1 - expected_score_blue
    if blue_win:
        elo[blue_id].elo = blue_elo + k_factor*(1-expected_score_blue)
        elo[red_id].elo = red_elo + k_factor*(0-expected_score_red)
    else:
        elo[blue_id].elo = blue_elo + k_factor*(0-expected_score_blue)
        elo[red_id].elo = red_elo + k_factor*(1-expected_score_red)


def calculate_elo(tournaments, tournament_id=None, startDate=datetime.now()):
    elo = init_elo()
    back_test = {}

    for tournament, league_id, game in tournaments.yield_games():
        if tournament_id and tournament["id"] != tournament_id:
            break
        tournament_start_date = datetime.strptime(tournament["startDate"], "%Y-%m-%d")
        days_since = (startDate- tournament_start_date).days
        if days_since > 700:
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
        if not league_id:
            raise "WAHT THE FUCK? WHAT THE FUUUCKKK!!!"    
        k_factor = league_points(league_id)

        update_elo(
            elo,
            blue_id,
            red_id,
            blue_elo,
            red_elo,
            blue_win,
            k_factor
        )
        elo[blue_id].games += 1
        elo[red_id].games += 1
        elo[blue_id].leagues.append(league_id)
        elo[red_id].leagues.append(league_id)
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

