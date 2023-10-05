from chalicelib.rankings import teams_by_elo, calculate_elo,get_tournament_teams
from chalicelib.esports import get_tournaments_data
from chalicelib.const import RANKINGS_BUCKET, RANKINGS_DIR, GLOBAL_RANKINGS_FILE
import json
import boto3

DATA_DIR = "chalicelib/data/"

s3 = boto3.resource('s3')

def upload_to_s3(json_data, file_name):
    s3object = s3.Object(RANKINGS_BUCKET, file_name)

    s3object.put(
        Body=(bytes(json.dumps(json_data).encode('UTF-8')))
    )

def generate_global_rankings():
    elo, _ = calculate_elo()
    rankings = list(i.json() for i in teams_by_elo(elo))
    with open("chalicelib/data/global.json", "w") as f:
        json.dump(rankings, f)
    upload_to_s3(rankings, GLOBAL_RANKINGS_FILE)
        
generate_global_rankings()


def generate_tournament_rankings():
    for tournament in get_tournaments_data():
        elo, _ = calculate_elo(tournament["id"])
        teams_sorted = teams_by_elo(elo)

        teams_in_tournament = list(get_tournament_teams(tournament))
        teams_sorted = [team for team in teams_sorted if team.id in teams_in_tournament]
        rankings = list(team.json() for team in teams_sorted)
        upload_to_s3(rankings, "%s%s.json" % (RANKINGS_DIR, tournament["id"]))
# generate_tournament_rankings()
