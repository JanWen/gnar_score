# load all the team ids from the json file and initialize a dictionary with each
# teams elo set to 1000

from chalicelib.esports import teams_data, leagues_data
from chalicelib.leagues import league_points #TODO CHECK IF NEEDED
from datetime import datetime
from chalicelib.team import Team
import json
from chalicelib.models.logger import log

# load all the team ids from the json file and initialize a dictionary with each
# teams elo set to 1000

BASE_ELO = 1500
DAYS_LIMIT = 360

K_FACTOR = 50

ML = True

mappings_data = None
with open("chalicelib/esports-data/mapping_data.json", "r") as json_file:
       mappings_data = json.load(json_file)

def get_tournament_league(tournament_id):
    for league in leagues_data:
        for tournaments in league["tournaments"]:
            if tournaments["id"] == tournament_id:
                return league["slug"]
            

def get_start_elo(league_slug):
    if league_slug == "lpl" or league_slug == "lck":
        return 1500
    if league_slug == "lcs" or league_slug == "lec":
        return 1200
    if not league_slug:
        return 800
    return BASE_ELO

def best_of_mod(k_factor, blue_game_wins, red_game_wins):
    if blue_game_wins + red_game_wins < 3:
        return 0.8*k_factor
    elif blue_game_wins + red_game_wins < 5:
        return 0.9*k_factor
    return k_factor
    
def tournament_mod(tournament, stage, k_factor):
    tournament_slug = tournament["slug"].lower()
    if tournament_slug.startswith("worlds") or tournament_slug.startswith("msi"):
        k_factor = 1.5*k_factor
    elif "spring" in tournament_slug or "summer" in tournament_slug:
        k_factor = 0.9*k_factor
    else:
        k_factor = 0.8*k_factor

    if stage.lower() in ["playoffs", "knockouts", "promotion series", "promotion"]:
        pass
    elif stage.lower() in ["groups", "regular season"]:
        k_factor = 0.9*k_factor
    elif stage.lower() in ["play in groups", "play_in_knockouts", "play_in_knockouts"]:
        k_factor = 0.8*k_factor
    else:
        k_factor = 0.7*k_factor
    return k_factor

def get_platformgameid(esportsgameid):
    for mapping in mappings_data:
        if mapping["esportsGameId"] == esportsgameid:
            return mapping["platformGameId"]



class Elo:
    def __init__(self, teams=None, kfactor=K_FACTOR) -> None:
        if teams:
            self.elo = {team.id:team for team in teams}
        else:
            self.elo = {}
        self.back_test = {}
        self.squared_errors = []
        self.squared_errors_pure = []

    def update_elo(
            self,
            blue_team,
            red_team,
            league_id,
            stage=None,
            tournament=None,
            k_factor=K_FACTOR,
            df=None,
            model=None,
            game_platform_ids=None
    ):
        stage = stage["name"].lower()
        blue_win = blue_team["result"]["outcome"] == "win"
        red_win = red_team["result"]["outcome"] == "win"
        blue_id = blue_team["id"]
        red_id = red_team["id"]
        blue_game_wins = blue_team["result"]["gameWins"]
        red_game_wins = red_team["result"]["gameWins"]

        model_prediction = None
        prob_blue = None
        prob_red = None
        if ML:
            if df is not None and any(game_platform_ids):
                games = df[df["platformgameid"].isin(game_platform_ids)]
                # blue_team_data = df[df["eventtime"] <= tournament["startDate"]]
                if len(games):
                    # games["eventtime"] = games["eventtime"].astype("string")
                    log.info("COCKTIME %s BALL TIME XD %s" % (games.iloc[[0]]["eventtime"], tournament["startDate"]) )

                    x = games.iloc[[0]][[
                        "blue_avg_inhib", "red_avg_inhib",
                        "blue_avg_tower", "red_avg_tower",
                        "blue_avg_kills", "red_avg_kills",
                        "blue_avg_win", "red_avg_win",
                        "red_avg_deaths", "blue_avg_deaths",
                        "blue_level", "red_level",
                        "blue_cs", "red_cs",
                        "blue_avg_kill", "red_avg_kill",
                    ]]
                    prob_blue, prob_red = model.predict_proba(x)[0]
                    prediction = model.predict(x)[0]
                    if prediction == 100:
                        model_prediction = 1
                    elif prediction == 200:
                        model_prediction = 0
                    # print(prediction)
        self.balls += 1
        league = get_tournament_league(tournament["id"])
        start_elo = BASE_ELO
        # start_elo = get_start_elo(league)
        
        if blue_team["id"] not in self.elo:
            self.elo[blue_team["id"]] = Team((blue_team["id"],start_elo))
        if red_team["id"] not in self.elo:
            self.elo[red_team["id"]] = Team((red_team["id"],start_elo))
        
        try: #TODO some chinese teams are not in the teams.json file
            blue_elo = self.elo[blue_id].elo
            red_elo = self.elo[red_id].elo
        except KeyError as e:
            return

        # k_factor = tournament_mod(tournament, stage, k_factor)
        # k_factor = best_of_mod(k_factor, blue_game_wins, red_game_wins)
        
        
        expected_score_blue = 1/(1+10**((red_elo-blue_elo)/480))
        expected_score_blue_pure = 1/(1+10**((red_elo-blue_elo)/480))
        expected_score_red = 1/(1+10**((blue_elo-red_elo)/480))
        expected_score_red_pure = 1/(1+10**((blue_elo-red_elo)/480))

        if model_prediction is not None:
            w = 0.5
            if prob_blue > 0.85 or prob_red > 0.85:
                w = max(prob_blue, prob_red)
            expected_score_blue = (w * expected_score_blue) + ((1 - w) * prob_blue)
            expected_score_red = (w * expected_score_red) + ((1 - w) * prob_red)

            # if prob_blue > 0.85 or prob_red > 0.85:
            #     k_factor = 1.5*k_factor

        blue_kfactor = k_factor
        red_kfactor = k_factor

        squared_error = None
        squared_error_pure = None
        if blue_win:
            squared_error = (expected_score_blue-1)**2 + (expected_score_red-0)**2
            squared_error_pure = (expected_score_blue_pure-1)**2 + (expected_score_red_pure-0)**2
            blue_kfactor = blue_kfactor * (1+0.8*(blue_game_wins-red_game_wins))
            red_kfactor = red_kfactor * (1+0.8*(blue_game_wins-red_game_wins))
            self.elo[blue_id].elo = blue_elo + (blue_kfactor*(1-expected_score_blue))
            self.elo[red_id].elo = red_elo + (red_kfactor*(0-expected_score_red))
        elif red_win:
            squared_error = (expected_score_blue-0)**2 + (expected_score_red-1)**2
            squared_error_pure = (expected_score_blue_pure-0)**2 + (expected_score_red_pure-1)**2
            blue_kfactor = blue_kfactor * (1+0.8*(red_game_wins-blue_game_wins))
            red_kfactor = red_kfactor * (1+0.8*(red_game_wins-blue_game_wins))
            self.elo[blue_id].elo = blue_elo + (blue_kfactor*(0-expected_score_blue))
            self.elo[red_id].elo = red_elo + (red_kfactor*(1-expected_score_red))
        if squared_error:
            self.squared_errors.append(squared_error)
        if squared_error_pure:
            self.squared_errors_pure.append(squared_error_pure)
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

def calculate_elo(tournaments, tournament_id=None, startDate=datetime.now(), k_factor=K_FACTOR, df=None,
            model=None):
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

        game_platform_ids = [get_platformgameid(game["id"]) for game in league_match["games"]]

            

        elo.update_elo(
            blue_team,
            red_team,
            league_id,
            stage,
            tournament,
            k_factor,
            df=df,
            model=model,
            game_platform_ids=game_platform_ids
        )
    mean_squared_error =  sum(elo.squared_errors)/len(elo.squared_errors) if elo.squared_errors else None
    mean_squared_error_pure = sum(elo.squared_errors_pure)/len(elo.squared_errors_pure) if elo.squared_errors_pure else None
    print("PURE MSR", len(elo.squared_errors_pure),mean_squared_error_pure)
    return elo.elo, elo.back_test, mean_squared_error
