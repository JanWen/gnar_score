from chalicelib.generate_rankings import generate_rankings
from chalicelib.tournaments import Tournaments
import json
from chalicelib.esports import leagues_data


tournaments = Tournaments()


print("Generating tournaments_ids.json")
def get_league(league_id):
    league = [league for league in leagues_data if league["id"] == league_id]
    if len(league) == 0:
        return None
    return league[0]["name"]


def get_tournaments_data(tournaments):
    for t in tournaments:
        name = None
        league_name = get_league(t["leagueId"])
        if league_name and not t["name"].startswith(league_name):
            name = league_name + " " + t["name"]
        yield {
            "id": t["id"],
            "name": name,
        }

with open("chalicelib/esports-data/tournaments_ids.json", "w") as json_file:
    json.dump(get_tournaments_data(tournaments), json_file)

print("Generating rankings.json")
# generate_rankings(tournaments)