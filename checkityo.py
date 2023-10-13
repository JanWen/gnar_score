from chalicelib.tournaments import Tournaments
from chalicelib.generate_rankings import teams_by_elo, get_tournament_teams
from chalicelib.elo import calculate_elo
from datetime import datetime
TOURNAMENT_ID = "110574243270525539"
from chalicelib.esports import teams_data


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

def team_data(team):
    team_win = team["result"]["outcome"] == "win"
    team_id = team["id"]
    team_game_wins = team["result"]["gameWins"]
    return team_win, team_id, team_game_wins

for tournament in tournaments.data:
    print(tournament["id"], tournament["name"])
    winners = {}

    for match in yield_matches(tournament):
        blue_team = match["teams"][0]
        blue_win, blue_id, blue_game_wins = team_data(blue_team)
        red_team = match["teams"][1]
        red_win, red_id, red_game_wins = team_data(red_team)
        blue_info = {}
        if [team for team in teams_data if team["team_id"] == blue_id]:
            blue_info = [team for team in teams_data if team["team_id"] == blue_id][0]
        red_info = {}
        if [team for team in teams_data if team["team_id"] == red_id]:
            red_info = [team for team in teams_data if team["team_id"] == red_id][0]

        if blue_win:
            if blue_id not in winners:
                winners[blue_id] = blue_info
                winners[blue_id]["wins"] = 0
            winners[blue_id]["wins"] += 1
        elif red_win:
            if red_id not in winners:
                winners[red_id] = red_info
                winners[red_id]["wins"] = 0
            winners[red_id]["wins"] += 1
    for winner in winners:
        print("\t",winner, winners[winner])
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
