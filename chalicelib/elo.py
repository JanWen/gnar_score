# load all the team ids from the json file and initialize a dictionary with each
# teams elo set to 1000

from chalicelib.esports import teams_data
from chalicelib.leagues import league_points #TODO CHECK IF NEEDE
from datetime import datetime
from chalicelib.team import Team

# load all the team ids from the json file and initialize a dictionary with each
# teams elo set to 1000

BASE_ELO = 1500
DAYS_LIMIT = 720

K_FACTOR = 50

def adjust_k_factor(k_factor, elo):
    # if elo > 1700:
    #     return k_factor - 20
    return k_factor

def adjust_k_factor_tennis(k_factor, elo):
    #https://www.ultimatetennisstatistics.com/blog?post=eloKfactorTweaks#
    ratio = 1+18/(1+2**((elo-1500)/63))
    return ratio * k_factor
    if elo > 2200:
        return 1.008*k_factor
    elif elo > 2000:
        return 1.07*k_factor
    elif elo > 1800:
        return 1.64*k_factor
    elif elo > 1600:
        return 5.5*k_factor
    elif elo > 1500:
        return 10*k_factor
    else:
        return 10*k_factor


class Elo:
    def __init__(self, teams=None, kfactor=K_FACTOR) -> None:
        if teams:
            self.elo = {team.id:team for team in teams}
        else:
            self.elo = {team["team_id"]:Team((team["team_id"],BASE_ELO)) for team in teams_data}
        self.back_test = {}
        self.squared_errors = []

    def update_elo(
            self,
            blue_team,
            red_team,
            league_id,
            stage=None,
            tournament=None,
    ):
        

        
        
        
        stage = stage["name"].lower()
        blue_win = blue_team["result"]["outcome"] == "win"
        red_win = red_team["result"]["outcome"] == "win"
        blue_id = blue_team["id"]
        red_id = red_team["id"]
        blue_game_wins = blue_team["result"]["gameWins"]
        red_game_wins = red_team["result"]["gameWins"]
        k_factor = K_FACTOR
        
        
        try: #TODO some chinese teams are not in the teams.json file
            blue_elo = self.elo[blue_id].elo
            red_elo = self.elo[red_id].elo
        except KeyError as e:
            return
        


        tournament_slug = tournament["slug"].lower()
        if tournament_slug.startswith("worlds") or tournament_slug.startswith("msi"):
            k_factor = 1.5*k_factor
        elif "spring" in tournament_slug or "summer" in tournament_slug:
            k_factor = 0.9*k_factor
        else:
            k_factor = 0.8*k_factor

        # if stage.lower() in ["playoffs", "knockouts", "promotion series", "promotion"]:
        #     pass
        # elif stage.lower() in ["groups", "regular season"]:
        #     k_factor = 0.9*k_factor
        # elif stage.lower() in ["play in groups", "play_in_knockouts", "play_in_knockouts"]:
        #     k_factor = 0.8*k_factor
        # else:
        #     k_factor = 0.7*k_factor


        # if blue_game_wins + red_game_wins < 3:
        #     k_factor = 0.8*k_factor
        # elif blue_game_wins + red_game_wins < 5:
        #     k_factor = 0.9*k_factor
        

        expected_score_blue = 1/(1+10**((red_elo-blue_elo)/400))
        expected_score_red = 1/(1+10**((blue_elo-red_elo)/400))

        blue_kfactor = adjust_k_factor(k_factor, blue_elo)
        red_kfactor = adjust_k_factor(k_factor, red_elo)

        # NEWBIE BONUS
        newbie_bonus = 30
        if self.elo[blue_id].matches < 5:
            blue_kfactor += newbie_bonus
        if self.elo[red_id].matches < 5:
            red_kfactor += newbie_bonus
        squared_error = None
        if blue_win:
            
            squared_error = (expected_score_blue-1)**2 + (expected_score_red-0)**2
            self.elo[blue_id].elo = blue_elo + (blue_kfactor*(1-expected_score_blue)
                                        *(1+0.12*(blue_game_wins-red_game_wins))
                                    )
            self.elo[red_id].elo = red_elo + (red_kfactor*(0-expected_score_red)
                                        *(1+0.12*(blue_game_wins-red_game_wins))
                                    )
        elif red_win:
            squared_error = (expected_score_blue-0)**2 + (expected_score_red-1)**2
            self.elo[blue_id].elo = blue_elo + (blue_kfactor*(0-expected_score_blue)
                                         *(1+0.12*(red_game_wins-blue_game_wins))       
                                )
            self.elo[red_id].elo = red_elo + (red_kfactor*(1-expected_score_red)
                                         *(1+0.12*(red_game_wins-blue_game_wins))       
                                              )
        if squared_error:
            self.squared_errors.append(squared_error)
        # back_test_elo()
        elo_diff = round(blue_elo - red_elo)
        if elo_diff not in self.back_test:
            self.back_test[elo_diff] = {
                "total": 1,
            }
            if blue_win:
                self.back_test[elo_diff]["blue_wins"] = 1
            else:
                self.back_test[elo_diff]["blue_wins"] = 0
        else:
            self.back_test[elo_diff]["total"] += 1
            if blue_win:
                self.back_test[elo_diff]["blue_wins"] += 1

        self.elo[blue_id].matches += 1
        self.elo[red_id].matches += 1
        self.elo[blue_id].leagues.append(league_id)
        self.elo[red_id].leagues.append(league_id)


function_by_score = {
    0: {
        1: lambda p: 1-p,
        2: lambda p: (1-p)**2,
        3: lambda p: (1-p)**3,
    },
    1: {
        0: lambda p: p,
        1: lambda p: p*(1-p),
        2: lambda p: 2*p*((1-p)**2),
        3: lambda p: 3*p*((1-p)**3),
    },
    2: {
        0: lambda p: p*p,
        1: lambda p: 2*p*p*(1-p),
        3: lambda p: (6*(1-p)**3)*p*p,
    },
    3: {
        0: lambda p: p*p*p,
        1: lambda p: 3*p*p*p*(1-p),
        2: lambda p: 6*p*p*p*((1-p)**2),
    }
}

def calculate_elo(tournaments, tournament_id=None, startDate=datetime.now(), k_factor=K_FACTOR):
    elo = Elo()

    for tournament,stage, league_match in tournaments.yield_matches():
        league_id = tournament["leagueId"]
        if tournament_id and (tournament["id"] == tournament_id):
            break
        tournament_start_date = datetime.strptime(tournament["startDate"], "%Y-%m-%d")
        days_since = (startDate- tournament_start_date).days
        if days_since > DAYS_LIMIT or tournament_start_date > startDate:
            continue

        blue_team = league_match["teams"][0]
        red_team = league_match["teams"][1]

        if blue_team["side"] != "blue":
            raise "FUCKING SHITBALL"
        
        elo.update_elo(
            blue_team,
            red_team,
            league_id,
            stage,
            tournament,
        )
        
    print("Square Error\n",K_FACTOR, sum(elo.squared_errors)/len(elo.squared_errors))
    
    return elo.elo, elo.back_test



