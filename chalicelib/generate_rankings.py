from chalicelib.elo import calculate_elo
from chalicelib.esports import get_tournaments_data
from chalicelib.const import RANKINGS_BUCKET, RANKINGS_DIR, GLOBAL_RANKINGS_FILE
from chalicelib.aws import s3
from chalicelib.tournaments import Tournaments
import json
from datetime import datetime

def save_locally(json_data, file_name):
    with open("chalicelib/"+file_name, "w") as json_file:
        json.dump(json_data, json_file)

def upload_to_s3(json_data, file_name):
    s3object = s3.Object(RANKINGS_BUCKET, file_name)

    s3object.put(
        Body=(bytes(json.dumps(json_data).encode('UTF-8')))
    )

def teams_by_elo(elo):
    return [team for _, team in sorted(elo.items(), key=lambda item: item[1].adjusted_elo(), reverse=True)]

def get_tournament_teams(tournament):
    for stage in tournament["stages"]:
        for section in stage["sections"]:
            for match in section["matches"]:
                if match["state"] == "completed":
                    for team in match["teams"]:
                        yield team["id"]

def generate_global_rankings(tournaments):
    elo, _ = calculate_elo(tournaments)
    rankings = list(i.json() for i in teams_by_elo(elo))
    return rankings    

def generate_tournament_rankings(tournaments):
    for tournament in tournaments.data:
        tournament_start_date = datetime.strptime(tournament["startDate"], "%Y-%m-%d")
        elo, _ = calculate_elo(tournaments, tournament["id"], tournament_start_date)
        teams_sorted = teams_by_elo(elo)
        teams_in_tournament = list(get_tournament_teams(tournament))
        teams_sorted = [team for team in teams_sorted if team.id in teams_in_tournament]
        rankings = list(team.json() for team in teams_sorted)
        yield tournament["id"], rankings
    
def generate_rankings():
    tournaments = Tournaments()
    global_rankings = generate_global_rankings(tournaments)
    upload_to_s3(global_rankings, GLOBAL_RANKINGS_FILE)
    for tournament_id, tounament_ranking in generate_tournament_rankings(tournaments):
        save_locally(tounament_ranking, "%s%s.json" % (RANKINGS_DIR, tournament_id))
        upload_to_s3(tounament_ranking, "%s%s.json" % (RANKINGS_DIR, tournament_id))
