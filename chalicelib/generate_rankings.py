from chalicelib.rankings import teams_by_elo, get_tournament_teams
from chalicelib.elo import calculate_elo
from chalicelib.esports import get_tournaments_data
from chalicelib.const import RANKINGS_BUCKET, RANKINGS_DIR, GLOBAL_RANKINGS_FILE
from chalicelib.aws import s3
from chalicelib.tournaments import Tournaments
import json


def upload_to_s3(json_data, file_name):
    s3object = s3.Object(RANKINGS_BUCKET, file_name)

    s3object.put(
        Body=(bytes(json.dumps(json_data).encode('UTF-8')))
    )

def generate_global_rankings(tournaments):
    elo, _ = calculate_elo(tournaments)
    rankings = list(i.json() for i in teams_by_elo(elo))
    return rankings    

def generate_tournament_rankings(tournaments):
    for tournament in tournaments.data:
        elo, _ = calculate_elo(tournaments, tournament["id"])
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
        upload_to_s3(tounament_ranking, "%s%s.json" % (RANKINGS_DIR, tournament_id))
