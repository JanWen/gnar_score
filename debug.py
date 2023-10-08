from chalicelib.tournaments import Tournaments
from chalicelib.generate_rankings import teams_by_elo, get_tournament_teams
from chalicelib.elo import calculate_elo
from datetime import datetime
TOURNAMENT_ID = "110535609415063567"


tournaments = Tournaments()

tournament = [tournament for tournament in tournaments.data if tournament["id"] == TOURNAMENT_ID][0]
tournament_start_date = datetime.strptime(tournament["startDate"], "%Y-%m-%d")
elo, _ = calculate_elo(tournaments, tournament["id"], tournament_start_date)
teams_sorted = teams_by_elo(elo)
teams_in_tournament = list(get_tournament_teams(tournament))
teams_sorted = [team for team in teams_sorted if team.id in teams_in_tournament]
rankings = list(team.json() for team in teams_sorted)

for i in rankings:
    print(i)
