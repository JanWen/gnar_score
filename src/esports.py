import json

def load_team_ids():
    with open("esports-data/teams.json", "r") as json_file:
        teams_data = json.load(json_file)
    return teams_data

def get_tournaments_data():
    tournaments_json = json.load(open("esports-data/tournaments.json", "r"))
    return sorted(tournaments_json, key=lambda item: item["startDate"])

teams_data = load_team_ids()
tournaments_data = get_tournaments_data()
