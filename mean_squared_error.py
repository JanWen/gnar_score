from chalicelib.elo import calculate_elo
from chalicelib.tournaments import Tournaments
import statistics
import os
import json
import matplotlib.pyplot as plt
from datetime import datetime
from chalicelib.generate_rankings import generate_global_rankings


# current date and time
now = datetime.now()

date_today = now.strftime("%d%m%Y")
results_dir = os.path.join("results", date_today)
try:
    os.mkdir(results_dir)
except FileExistsError:
    pass



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


def print_elo(elo):
    # sort dictionary by values
    
    with open(results_dir + "/elo.txt", "w", encoding="utf-8") as f:
        f.write("MIN ELO: %d \n" % min([i[1].elo for i in elo.items()]))
        f.write("AVERAGE ELO: %d \n" % (sum([i[1].elo for i in elo.items()])/len(elo)))
        f.write("MEDIAN ELO: %d \n" % statistics.median([i[1].elo for i in elo.items()]))
        f.write("MAX ELO: %d \n" % max([i[1].elo for i in elo.items()]))
        f.write("\n")
        for _, team in sorted(elo.items(), key=lambda item: -1*item[1].elo):
            f.write(str(team) + "\n", )

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
    elo_items = sorted(elo.items(), key=lambda item: item[1].elo)
    

    x = list(range(100, 3000, 100))
    y = [len([i[1] for i in elo_items if i[1].elo >= r and i[1].elo < r+100]) for r in x]
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
tournaments = Tournaments()

K_FACTOR = 55

import pandas as pd
from sklearn.naive_bayes import GaussianNB
import numpy as np

from chalicelib.model import load_model

print("Elo wihtou ML")
df, features, model = load_model()
elo, back_test, msr = calculate_elo(
    tournaments,
    k_factor=K_FACTOR,
    df = df,
    model = model,
    features=features,
)
print("MSR", msr)
print_elo(elo)

# ELO with ML
print("Elo with ML")
df, features, model = load_model()
elo, back_test, msr = calculate_elo(
    tournaments,
    k_factor=K_FACTOR,
    df = df,
    model = model,
    features=features,
    ml=True,
)
print("MSR", msr)
print_elo(elo)


# half_match_cutoff = get_elo_cutoff(back_test, 0.5)
# print("half_match_cutoff", half_match_cutoff)
# print_backtest(back_test, half_match_cutoff)
# team_elodiff(elo)

global_rankings = generate_global_rankings(elo)
for i in range(len(global_rankings)):
    global_rankings[i]["rank"] = i+1
with open(results_dir + "/global_ranking.json", "w", encoding="utf-8") as f:
    json.dump(global_rankings, f, indent=4)
elodiff_prediction_distribution()
