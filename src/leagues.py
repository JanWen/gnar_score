import json
import logging

log = logging.getLogger(__name__)
leagues_data = json.load(open("esports-data/leagues.json", "r"))

league_dict = {
    "international": ["Worlds", "MSI"],
    "major_east": ["LPL","LCK"],
    "major_west": [ "LEC","LCS"],
    "minor": ["CBLOL", "LCL", "LCO", "LJL", "LLA", "PCS", "TCL", "VCS"],
    "challenger": ["LCK Challengers", "EMEA Masters", "LCS Challengers Qualifiers", "LCS Challengers"],
    "regional": ["Ultraliga", "Prime League", "College Championship", "All-Star Event", "La Ligue FranÃ§aise", "NLC", "Elite Series", "Liga Portuguesa", "PG Nationals", "SuperLiga", "Hitpoint Masters", "Esports Balkan League", "Greek Legends League", "Arabian League", "LCK Academy", "LJL Academy", "CBLOL Academy", "North Regional League", "South Regional League", "TFT Rising Legends"]
}

def get_leagues():
    return leagues_data

region_elo_ratio = {
    "international": 1.0, #TODO why is this needed?
    "major_east": 1.0,
    "major_west": 0.9,
    "minor": 0.7,
    "challenger": 0.5,
    "regional": 0.3
}

points_mapping = {
    "international": 100,
    "major_east": 80,
    "major_west": 70,
    "minor": 60,
    "challenger": 40,
    "regional": 20
}

def get_league_elo_ratio(league_name):
    try:
        league_region = [key for key, value in league_dict.items() if league_name in value][0]
    except IndexError:  
        log.debug(f"League {league_name} not found in the leagues table")
        return 0
    return region_elo_ratio[league_region]


def get_league_name(league_id):
    try:
        league = [league for league in leagues_data if league["id"] == league_id][0]
    except IndexError:
        log.debug(f"League {league_id} not found in the leagues table")
        return "UNKNOWN"
    return league["name"]


def league_points(league_id):
    leagues = get_leagues()
    try:
        league = [league for league in leagues if league["id"] == league_id][0]
    except IndexError:
        log.debug(f"League {league_id} not found in the leagues table")
        return 0
    
    league_region = [key for key, value in league_dict.items() if league["name"] in value][0]
    

    return points_mapping[league_region]