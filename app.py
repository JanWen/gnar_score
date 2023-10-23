from chalice import Chalice
import logging, json
from chalicelib.aws import s3_client
from chalicelib.const import RANKINGS_BUCKET, GLOBAL_RANKINGS_FILE
from chalicelib.esports import teams_data

log = logging.getLogger(__name__)

app = Chalice(app_name='power_ranking')

@app.route('/')
def index():
    return global_rankings()


def rank_teams(teams_sorted):
    for i, team in enumerate(teams_sorted):
        team["rank"] = i + 1
        yield team


@app.route('/global_rankings', cors=True)
def global_rankings():
    """
    Global rankings - get current top X teams globally
    Query params:
        number_of_teams: number of teams to return
    """
    number_of_teams = 20
    if app.current_request.query_params:
        if app.current_request.query_params.get('number_of_teams'):
            number_of_teams = int(app.current_request.query_params.get('number_of_teams'))
    obj = s3_client.get_object(Bucket=RANKINGS_BUCKET, Key=GLOBAL_RANKINGS_FILE)
    data = obj['Body'].read().decode('utf-8')
    data = json.loads(data)
    return list(
        rank_teams(data)
    )[:number_of_teams]

@app.route('/tournament_rankings/{tournament_id}', cors=True)
def tournament_rankings(tournament_id):
    """
    Tournament rankings - get team rankings for a given tournament
    Params:
        tournament_id string (path) *required ID of tournament to return rankings for
        stage string (query) Stage of tournament to return rankings for
    """
    
    obj = s3_client.get_object(Bucket=RANKINGS_BUCKET, Key="rankings/"+tournament_id+".json")
    data = obj['Body'].read().decode('utf-8')
    data = json.loads(data)
    return list(
        rank_teams(data)
    )

@app.route('/team_rankings', cors=True)
def team_rankings():
    """
    Get ranking for a list of teams
    Params:
        team_ids array[string] (query) *required IDs of tournaments to return ranking for
    """
    team_ids = []
    #TODO looks ugly
    if app.current_request.query_params:
        if app.current_request.query_params.get('team_ids'):
            team_ids = app.current_request.query_params.get('team_ids').split(",")
            team_ids = [i.strip() for i in team_ids]
    if team_ids:
        obj = s3_client.get_object(Bucket=RANKINGS_BUCKET, Key=GLOBAL_RANKINGS_FILE)
        data = obj['Body'].read().decode('utf-8')
        data = json.loads(data)
        team_rankings = [team for team in data if team["team_id"] in team_ids]
        return list(rank_teams(team_rankings))
    
    return {"error": "Please provide team_ids query param (comma separated list of team ids)"}


@app.route('/teams', cors=True)
def team_rankings():
    return teams_data

@app.route('/tournaments', cors=True)
def team_rankings():
    tournaments = None
    with open("chalicelib/esports-data/tournaments_ids.json", "r") as json_file:
        tournaments = json.load(json_file)
    return tournaments