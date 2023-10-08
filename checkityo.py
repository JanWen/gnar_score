from chalicelib.tournaments import Tournaments
from chalicelib.generate_rankings import teams_by_elo, get_tournament_teams
from chalicelib.elo import calculate_elo
from datetime import datetime
TOURNAMENT_ID = "110574243270525539"


tournaments = Tournaments()


def tournament_elo(tournament):
    tournament_start_date = datetime.strptime(tournament["startDate"], "%Y-%m-%d")
    elo, _ = calculate_elo(tournaments, tournament["id"], tournament_start_date)
    teams_sorted = teams_by_elo(elo)
    teams_in_tournament = list(get_tournament_teams(tournament))
    teams_sorted = [team for team in teams_sorted if team.id in teams_in_tournament]
    return list(team.json() for team in teams_sorted)


def yield_matches(tournament):
    for stage in tournament["stages"]:
        for section in stage["sections"]:
            for match in section["matches"]:
                if match["state"] == "completed":
                    yield match

for tournament in tournaments.data:
    print(tournament["id"], tournament["name"])
    for match in yield_matches(tournament):
        print("\t",match["id"], match["name"])
    for team in tournament_elo(tournament):
        print("\t",team["team_name"], team["elo"])


# tournament = [tournament for tournament in tournaments.data if tournament["id"] == TOURNAMENT_ID][0]
# tournament_start_date = datetime.strptime(tournament["startDate"], "%Y-%m-%d")
# elo, _ = calculate_elo(tournaments, tournament["id"], tournament_start_date)
# teams_sorted = teams_by_elo(elo)
# teams_in_tournament = list(get_tournament_teams(tournament))
# teams_sorted = [team for team in teams_sorted if team.id in teams_in_tournament]
# rankings = list(team.json() for team in teams_sorted)

# for i in rankings:
#     print(i)
