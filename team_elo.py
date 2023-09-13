# load all the team ids from the json file and initialize a dictionary with each
# teams elo set to 1000

import json
import matplotlib.pyplot as plt

tournaments_data = json.load(open("esports-data/tournaments.json", "r"))

def load_team_ids():
    with open("esports-data/teams.json", "r") as json_file:
        teams_data = json.load(json_file)
    return teams_data

teams_data = load_team_ids()

def update_elo(
    elo,
    blue_id,
    red_id,
    blue_elo,
    red_elo,
    blue_win
):
    # calculate elo
    kitty = 5/100 * (blue_elo + red_elo)
    elo[blue_id] -= 5/100 * blue_elo
    elo[red_id] -= 5/100 * red_elo

    if blue_win:
        elo[blue_id] += kitty
    else:
        elo[red_id] += kitty

def yield_games():
    for tournament in tournaments_data:
        for stage in tournament["stages"]:
            for section in stage["sections"]:
                for match in section["matches"]:
                    if match["state"] == "completed":
                        for game in match["games"]:
                            if game["state"] == "completed":
                                yield game

def calculate_elo():
    elo = {team["team_id"]:1000 for team in teams_data}
    back_test = {}

    for game in yield_games():
        blue_id = game["teams"][0]["id"]
        red_id = game["teams"][1]["id"]
        blue_win = game["teams"][0]["result"]["outcome"] == "win"
        try: # todo some chinese teams are not in the teams.json file
            blue_elo = elo[blue_id]
            red_elo = elo[red_id]
        except KeyError as e:
            continue
        
        
        # backtest_elo()
        elo_diff = round(blue_elo - red_elo)
        if elo_diff not in back_test:
            back_test[elo_diff] = {
                "total": 1,
            }
            if blue_win:
                back_test[elo_diff]["blue_wins"] = 1
            else:
                back_test[elo_diff]["blue_wins"] = 0
        else:
            back_test[elo_diff]["total"] += 1
            if blue_win:
                back_test[elo_diff]["blue_wins"] += 1
            

        update_elo(
            elo,
            blue_id,
            red_id,
            blue_elo,
            red_elo,
            blue_win
        )
        # check if blue tuple is really blue
        if game["teams"][0]["side"] != "blue":
            raise "FUCKING SHITBALL"
    
    return elo, back_test


def get_elo_cutoff(back_test, percentage):
    # get the elo score diff cut off at wich x% of games are included
    total_games = sum([i[1]["total"] for i in back_test.items()])
    cutoff = percentage * total_games
    print("total games", total_games)
    index = 1
    max_index = max(back_test.keys())
    while True:
        games_in_range = sum([i[1]["total"] for i in back_test.items() if i[0] > -1*index and i[0] < index])
        if games_in_range > cutoff or index > max_index:
            return index
        index += 1


class Team:
    def __init__(self, elo_tuple):
        self.id = elo_tuple[0]
        self.elo = elo_tuple[1]
        self.team_info = [team for team in teams_data if team["team_id"] == self.id]
        if len(self.team_info):
            self.team_name = self.team_info[0]["name"]
        else:
            self.team_name = "UNKNOWN"

    
    def __repr__(self) -> str:
        return "%s %s" % (self.team_name, self.elo)

def print_elo(elo):
    # sort dictionary by values
    print("### ELO")
    for team in sorted(elo.items(), key=lambda item: item[1]):
        t = Team(team)
        print(t)

def print_backtest(back_test, even_match_cutoff):
    # sort dictionary by values
    print("### BACKTEST")
    even_matches = [i for i in back_test.items() if i[0] > -even_match_cutoff and i[0] < even_match_cutoff]
    even_matches_total = sum([i[1]["total"] for i in even_matches])
    even_matchs_wr = sum([i[1]["blue_wins"] for i in even_matches]) / even_matches_total

    bluefav_matches = [i for i in back_test.items() if i[0] > even_match_cutoff]
    bluefav_matches_total = sum([i[1]["total"] for i in bluefav_matches])
    bluefav_wr = sum([i[1]["blue_wins"] for i in bluefav_matches]) / bluefav_matches_total

    redfav_matches = [i for i in back_test.items() if i[0] < -even_match_cutoff]
    redfav_matches_total = sum([i[1]["total"] for i in redfav_matches])
    redfav_wr = sum([i[1]["blue_wins"] for i in redfav_matches]) / redfav_matches_total
    
    print("EVEN MATCHES WR", round(even_matchs_wr, 2),even_matches_total)
    print("bluefav_matches WR", round(bluefav_wr, 2), bluefav_matches_total)
    print("redfav_matches WR", round(redfav_wr, 2), redfav_matches_total)

elo, back_test = calculate_elo()
print_elo(elo)

half_match_cutoff = get_elo_cutoff(back_test, 0.5)
print("half_match_cutoff", half_match_cutoff)
print_backtest(back_test, half_match_cutoff)


fig, ax = plt.subplots()
    # Plot the data

    # Set the title and axis labels
ax.set_title(f'wins distribution')
ax.set_xlabel('Score')
ax.set_ylabel('Winrate')

# coef = np.polyfit(superiority[0],superiority[i+1],2)
# print(j, coef)
# poly1d_fn = np.poly1d(coef)

back_test_items = sorted(back_test.items(), key=lambda item: item[0])
scores = [i[0] for i in back_test_items]
total = [i[1]["total"] for i in back_test_items]
ax.plot(
    scores,
    total,
    # [i[0] for i in back_test.items()],
    # poly1d_fn(superiority[0]),
    #'--k'
)
plt.show()