# load all the team ids from the json file and initialize a dictionary with each
# teams elo set to 1000

from chalicelib.esports import teams_data
from chalicelib.leagues import league_points #TODO CHECK IF NEEDE
from datetime import datetime
from chalicelib.team import Team

# load all the team ids from the json file and initialize a dictionary with each
# teams elo set to 1000

BASE_ELO = 1000
K_FACTOR = 50
DAYS_LIMIT = 180


class Elo:
    def __init__(self) -> None:
        self.elo = {team["team_id"]:Team((team["team_id"],BASE_ELO)) for team in teams_data}

    def update_elo(self, tournament, startDate=datetime.now()):
        tournament_id = tournament["id"]
        league_id = tournament["leagueId"]
        if tournament_id and tournament["id"] != tournament_id:
            return
        tournament_start_date = datetime.strptime(tournament["startDate"], "%Y-%m-%d")
        days_since = (startDate- tournament_start_date).days
        if days_since > DAYS_LIMIT:
            return

        for league_match in tournament["matches"]:
            blue_team = league_match["teams"][0]
            blue_id = blue_team["id"]
            red_team = league_match["teams"][1]
            red_id = red_team["id"]
            blue_win = blue_team["result"]["outcome"] == "win"
            blue_game_wins = blue_team["result"]["gameWins"]
            red_game_wins = red_team["result"]["gameWins"]
            if blue_team["side"] != "blue":
                raise "FUCKING SHITBALL"
            try: # TODO some chinese teams are not in the teams.json file
                blue_elo = self.elo[blue_id].elo
                red_elo = self.elo[red_id].elo
            except KeyError as e:
                continue
            
            k_factor = league_points(league_id) #TODO CHECK IF NEEDED

            if not k_factor:
                k_factor = K_FACTOR
            
            if blue_win:
                expected_score_blue = 1/(1+10**((red_elo-blue_elo)/480))
                expected_score_blue = function_by_score[blue_game_wins][red_game_wins](expected_score_blue)
                expected_score_red = 1 - expected_score_blue
                self.elo[blue_id].elo = blue_elo + k_factor*(1-expected_score_blue)
                self.elo[red_id].elo = red_elo + k_factor*(0-expected_score_red)
            else:
                expected_score_red = 1/(1+10**((blue_elo-red_elo)/480))
                try:
                    expected_score_red = function_by_score[red_game_wins][blue_game_wins](expected_score_red)
                except Exception as e:
                    print(red_game_wins, blue_game_wins, expected_score_red, league_match["id"])
                    raise "FUUSASDLHKSD"
                expected_score_blue = 1 - expected_score_red
                self.elo[blue_id].elo = blue_elo + k_factor*(0-expected_score_blue)
                self.elo[red_id].elo = red_elo + k_factor*(1-expected_score_red)

            self.elo[blue_id].games += 1
            self.elo[red_id].games += 1
            self.elo[blue_id].leagues.append(league_id)
            self.elo[red_id].leagues.append(league_id)

            return self.elo, {}


def init_elo():
    return {team["team_id"]:Team((team["team_id"],BASE_ELO)) for team in teams_data}

function_by_score = {
    1: {
        0: lambda p: p,
        1: lambda p: p*(1-p),
    },
    2: {
        0: lambda p: p*p,
        1: lambda p: 2*p*p*(1-p),
    },
    3: {
        0: lambda p: p*p*p,
        1: lambda p: 3*p*p*p*(1-p),
        2: lambda p: 6*p*p*p*((1-p)**2),
    }
}

def calculate_elo(tournaments, tournament_id=None, startDate=datetime.now()):
    elo = init_elo()
    back_test = {}

    for tournament, league_match in tournaments.yield_matches():
        league_id = tournament["leagueId"]
        if tournament_id and tournament["id"] != tournament_id:
            break
        tournament_start_date = datetime.strptime(tournament["startDate"], "%Y-%m-%d")
        days_since = (startDate- tournament_start_date).days
        if days_since > DAYS_LIMIT:
            continue

        blue_team = league_match["teams"][0]
        blue_id = blue_team["id"]
        red_team = league_match["teams"][1]
        red_id = red_team["id"]
        blue_win = blue_team["result"]["outcome"] == "win"
        blue_game_wins = blue_team["result"]["gameWins"]
        red_game_wins = red_team["result"]["gameWins"]
        if blue_team["side"] != "blue":
            raise "FUCKING SHITBALL"
        try: # todo some chinese teams are not in the teams.json file
            blue_elo = elo[blue_id].elo
            red_elo = elo[red_id].elo
        except KeyError as e:
            continue
        
        # k_factor = league_points(league_id)

        # if not k_factor:
        k_factor = K_FACTOR
        
        if blue_win:
            expected_score_blue = 1/(1+10**((red_elo-blue_elo)/480))
            expected_score_blue = function_by_score[blue_game_wins][red_game_wins](expected_score_blue)
            expected_score_red = 1 - expected_score_blue
            elo[blue_id].elo = blue_elo + k_factor*(1-expected_score_blue)
            elo[red_id].elo = red_elo + k_factor*(0-expected_score_red)
        else:
            expected_score_red = 1/(1+10**((blue_elo-red_elo)/480))
            try:
                expected_score_red = function_by_score[red_game_wins][blue_game_wins](expected_score_red)
            except Exception as e:
                print(red_game_wins, blue_game_wins, expected_score_red, league_match["id"])
                raise "FUUSASDLHKSD"
            expected_score_blue = 1 - expected_score_red
            elo[blue_id].elo = blue_elo + k_factor*(0-expected_score_blue)
            elo[red_id].elo = red_elo + k_factor*(1-expected_score_red)

        elo[blue_id].games += 1
        elo[red_id].games += 1
        elo[blue_id].leagues.append(league_id)
        elo[red_id].leagues.append(league_id)
        # check if blue tuple is really blue
        
    
    return elo, back_test



