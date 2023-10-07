from chalicelib.elo import calculate_elo
from chalicelib.tournaments import Tournaments


def rank_teams(teams_sorted):
    for i, team in enumerate(teams_sorted):
        team.rank = i + 1
        yield team


def teams_by_elo(elo):
    return [team for _, team in sorted(elo.items(), key=lambda item: item[1].adjusted_elo(), reverse=True)]
     

def global_rankings(tournaments):
    elo, _ = calculate_elo(tournaments)
    teams_sorted = teams_by_elo(elo)
    return rank_teams(teams_sorted)

def team_rankings(tournaments, team_ids):
    elo, _ = calculate_elo(tournaments)
    teams_sorted = [team for team in teams_by_elo(elo) if team.id in team_ids]
    return rank_teams(teams_sorted)


def get_tournament_teams(tournament):
    for stage in tournament["stages"]:
        for section in stage["sections"]:
            for match in section["matches"]:
                if match["state"] == "completed":
                    for team in match["teams"]:
                        yield team["id"]

def tournament_rankings(tournaments, tournament_id):
    elo, _ = calculate_elo(tournaments, tournament_id)
    teams_sorted = teams_by_elo(elo)

    tournament = [tournament for tournament in tournaments.data if tournament["id"] == tournament_id][0]
    teams_in_tournament = list(get_tournament_teams(tournament))
    teams_sorted = [team for team in teams_sorted if team.id in teams_in_tournament]
    return rank_teams(teams_sorted)