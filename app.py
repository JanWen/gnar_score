from chalice import Chalice
from src import team_elo

app = Chalice(app_name='power_ranking')


@app.route('/')
def index():
    rankings = [
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
    return rankings

@app.route('/global_rankings')
def global_rankings():
    """
    Global rankings - get current top X teams globally
    Query params:
        number_of_teams: number of teams to return
    """
    number_of_teams = 20
    
    #TODO looks like shit
    if app.current_request.query_params:
        if app.current_request.query_params.get('number_of_teams'):
            #TODO try except in case query param is some bullshit
            number_of_teams = int(app.current_request.query_params.get('number_of_teams'))

    rankings = list(
        team.json() for team in team_elo.global_rankings()
    )[:number_of_teams]
    return rankings

@app.route('/tournament_rankings/{tournament_id}')
def tournament_rankings(tournament_id):
    """
    Tournament rankings - get team rankings for a given tournament
    Params:
        tournament_id string (path) *required ID of tournament to return rankings for
        stage string (query) Stage of tournament to return rankings for
    """
    
    return list(team.json() for team in team_elo.tournament_rankings(tournament_id))

@app.route('/team_rankings')
def team_rankings():
    """
    Tournament rankings - get team rankings for a given tournament
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
        return list(team.json() for team in team_elo.team_rankings(team_ids))
    
    return {"error": "Please provide team_ids query param (comma separated list of team ids)"}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
