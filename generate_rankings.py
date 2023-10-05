from chalicelib.rankings import teams_by_elo, calculate_elo,get_tournament_teams
from chalicelib.esports import get_tournaments_data
from chalicelib.const import RANKINGS_BUCKET, RANKINGS_DIR, GLOBAL_RANKINGS_FILE
from chalicelib.aws import s3
import json


def upload_to_s3(json_data, file_name):
    s3object = s3.Object(RANKINGS_BUCKET, file_name)

    s3object.put(
        Body=(bytes(json.dumps(json_data).encode('UTF-8')))
    )

def generate_global_rankings():
    elo, _ = calculate_elo()
    rankings = list(i.json() for i in teams_by_elo(elo))
    return rankings    

def generate_tournament_rankings():
    for tournament in get_tournaments_data():
        elo, _ = calculate_elo(tournament["id"])
        teams_sorted = teams_by_elo(elo)

        teams_in_tournament = list(get_tournament_teams(tournament))
        teams_sorted = [team for team in teams_sorted if team.id in teams_in_tournament]
        rankings = list(team.json() for team in teams_sorted)
        return tournament["id"], rankings
    
def generate_rankings():
    global_rankings = generate_global_rankings()
    upload_to_s3(global_rankings, GLOBAL_RANKINGS_FILE)
    for tournament_id, tounament_ranking in generate_tournament_rankings():
        upload_to_s3(tounament_ranking, "%s%s.json" % (RANKINGS_DIR, tournament_id))
