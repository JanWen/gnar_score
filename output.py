from team_elo import calculate_elo, get_elo_cutoff
from esports import teams_data
import statistics
import os
import matplotlib.pyplot as plt
from datetime import datetime


# current date and time
now = datetime.now()

date_today = now.strftime("%d%m%Y")
results_dir = os.path.join("results", date_today)
try:
    os.mkdir(results_dir)
except FileExistsError:
    pass

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
    
    with open(results_dir + "/elo.txt", "w") as f:
        f.write("MIN ELO: %d \n" % min([i[1] for i in elo.items()]))
        f.write("AVERAGE ELO: %d \n" % (sum([i[1] for i in elo.items()])/len(elo)))
        f.write("MEDIAN ELO: %d \n" % statistics.median([i[1] for i in elo.items()]))
        f.write("MAX ELO: %d \n" % max([i[1] for i in elo.items()]))
        f.write("\n")
        for team in sorted(elo.items(), key=lambda item: item[1]):
            t = Team(team)
            f.write(str(t) + "\n")

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

import seaborn as sns

def team_elodiff(elo):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(40, 24), dpi=80)
    elo_items = sorted(elo.items(), key=lambda item: item[1])
    

    x = list(range(100, 3000, 100))
    y = [len([i[1] for i in elo_items if i[1] >= r and i[1] < r+100]) for r in x]
    # plt.ylim(min(y), max(y))

    sns.barplot(x=x, y=y)
    plt.xticks(rotation=30, horizontalalignment='right')
    plt.tight_layout()
    plt.savefig(results_dir + "/team_elo_distribution.png")
    #plt.show()

def elodiff_prediction_distribution():
    plt.figure(figsize=(40, 24), dpi=80)
    back_test_items = sorted(back_test.items(), key=lambda item: item[0])
    scores = [i[0] for i in back_test_items]
    total = [i[1]["total"] for i in back_test_items]
    sns.lineplot(
        x=scores,
        y=total,
    )
    plt.xticks(rotation=30, horizontalalignment='right')
    plt.tight_layout()
    plt.savefig(results_dir + "/games_per_elodiff.png")
    #plt.show()


elo, back_test = calculate_elo()
print_elo(elo)

half_match_cutoff = get_elo_cutoff(back_test, 0.5)
print("half_match_cutoff", half_match_cutoff)
print_backtest(back_test, half_match_cutoff)
team_elodiff(elo)
elodiff_prediction_distribution()
