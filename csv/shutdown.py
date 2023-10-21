import csv
from chalicelib.esports import teams_data
import json

team_shutdown_ratio = {}

with open("shutdown.csv", "r") as f:
    csvr = csv.reader(f, delimiter=',')
    next(csvr, None)
    for line in csvr:
        platformgameid, teamid, side, shutdown_collected, blue_max_shutdown, red_max_shutdown = line
        if not shutdown_collected:
            shutdown_collected = 0
        if side == "100":
            blue_max_shutdown = float(blue_max_shutdown)
            if not blue_max_shutdown:
                continue
            shutdown_ratio = float(shutdown_collected)/float(blue_max_shutdown)
            if teamid not in team_shutdown_ratio:
                team_shutdown_ratio[teamid] = [shutdown_ratio]
            else:
                team_shutdown_ratio[teamid].append(shutdown_ratio)
        else:
            red_max_shutdown = float(red_max_shutdown)
            if not red_max_shutdown:
                continue
            shutdown_ratio = float(shutdown_collected)/float(red_max_shutdown)
            if teamid not in team_shutdown_ratio:
                team_shutdown_ratio[teamid] = [shutdown_ratio]
            else:
                team_shutdown_ratio[teamid].append(shutdown_ratio)


global_rankings = []
with open("results/19102023/global_ranking.json", "r") as f:
    global_rankings = json.load(f)


for teamid, ratios in team_shutdown_ratio.items():
    ratio = sum(ratios)/len(ratios)
    team = [team for team in teams_data if team["team_id"] == teamid]
    if not team:
        continue
    league = [team for team in global_rankings if team["team_id"] == teamid]
    if not league:
        continue
    row = "%s,%s,%s" % (team[0]["name"], league[0]["league"], ratio)
    print(row)