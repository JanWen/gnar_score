import json

def load_team_ids():
    with open("esports-data/teams.json", "r") as json_file:
        teams_data = json.load(json_file)
    return teams_data

tournaments_data = json.load(open("esports-data/tournaments.json", "r"))
teams_data = load_team_ids()

