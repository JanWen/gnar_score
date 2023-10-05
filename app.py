from chalice import Chalice
from chalicelib import rankings
import logging, json
from chalicelib.aws import s3
from chalicelib.const import RANKINGS_BUCKET, GLOBAL_RANKINGS_FILE

log = logging.getLogger(__name__)

app = Chalice(app_name='power_ranking')

@app.route('/')
def index():
    example_rankings = [
        {
            "team_id": "100205573495116443",
            "team_code": "GEN",
            "team_name": "Gen.G",
            "rank": 1
        },
        {
            "team_id": "98767991877340524",
            "team_code": "C9",
            "team_name": "Cloud9",
            "rank": 1
        },
        {
            "team_id": "99566404853058754",
            "team_code": "WBG",
            "team_name": "WeiboGaming FAW AUDI",
            "rank": 3
        }
    ]
    return example_rankings


def rank_teams(teams_sorted):
    for i, team in enumerate(teams_sorted):
        team["rank"] = i + 1
        yield team


@app.route('/global_rankings')
def global_rankings():
    """
    Global rankings - get current top X teams globally
    Query params:
        number_of_teams: number of teams to return
    """
    number_of_teams = 20
    obj = s3.get_object(Bucket=RANKINGS_BUCKET, Key=GLOBAL_RANKINGS_FILE)
    data = obj['Body'].read().decode('utf-8')
    data = json.loads(data)
    return list(
        rank_teams(data)
    )[:number_of_teams]

@app.route('/tournament_rankings/{tournament_id}')
def tournament_rankings(tournament_id):
    """
    Tournament rankings - get team rankings for a given tournament
    Params:
        tournament_id string (path) *required ID of tournament to return rankings for
        stage string (query) Stage of tournament to return rankings for
    """
    
    obj = s3.get_object(Bucket=RANKINGS_BUCKET, Key="rankings/"+tournament_id+".json")
    data = obj['Body'].read().decode('utf-8')
    data = json.loads(data)
    return list(
        rank_teams(data)
    )

@app.route('/team_rankings')
def team_rankings():
    """
    Get ranking for a list of teams
    Params:
        team_ids array[string] (query) *required IDs of tournaments to return ranking for
    """
    team_ids = []
    #TODO looks like shit
    if app.current_request.query_params:
        if app.current_request.query_params.get('team_ids'):
            #TODO try except in case query param is some bullshit
            team_ids = app.current_request.query_params.get('team_ids').split(",")
            team_ids = [i.strip() for i in team_ids]
    if team_ids:
        return list(team.json() for team in rankings.team_rankings(team_ids))
    
    return {"error": "Please provide team_ids query param (comma separated list of team ids)"}

