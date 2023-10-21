
from sklearn.neural_network import MLPClassifier
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

def roll_avg_kda():
    wins = pd.read_csv('csv/wins.csv')

    rolling_avg = pd.read_csv("csv/kd_rolling_avg.csv")
    rolling_avg = wins.merge(rolling_avg, on="platformgameid")

    print(rolling_avg)

    blue_side = rolling_avg[rolling_avg["side"] == 100]
    blue_side.rename(columns={
        "teamid": "blue_teamid",
        "avg_kills": "blue_avg_kills",
        "avg_deaths": "blue_avg_deaths",
        "avg_win": "blue_avg_win",
    }, inplace=True)
    blue_side.drop(columns=["side"], inplace=True)

    red_side = rolling_avg[rolling_avg["side"] == 200]
    red_side.rename(columns={
        "teamid": "red_teamid",
        "avg_kills": "red_avg_kills",
        "avg_deaths": "red_avg_deaths",
        "avg_win": "red_avg_win",
    }, inplace=True)
    red_side.drop(columns=["side", "winningteam"], inplace=True)


    joined = blue_side.merge(red_side, on="platformgameid")

    print(joined)
    X = joined[["blue_avg_kills", "blue_avg_deaths", "red_avg_kills", "red_avg_deaths"]]
    y = joined["winningteam"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    gnb = GaussianNB()
    model = gnb.fit(X_train, y_train)
    predictive_labels = gnb.predict(X_test)
    # print(predictive_labels)
    print(accuracy_score(y_test, predictive_labels))


def roll_avg_first_tower():

    first_buildings = pd.read_csv("csv/first_buildings.csv")
    print(first_buildings)


    # first inhib
    first_inhib = first_buildings[first_buildings["buildingtype"] == "inhibitor"]
    first_inhib = first_inhib.sort_values(by=['platformgameid', 'gametime'])
    first_inhib["killerteamid_inhib"] = first_inhib["teamid"].apply(lambda x: 200 if x == 100 else 100)
    first_inhib.drop_duplicates(subset=['platformgameid'], keep='first', inplace=True)
    first_inhib.drop(columns=["buildingtype", "teamid"], inplace=True)


    #first tower
    first_tower = first_buildings[first_buildings["buildingtype"] == "turret"]
    first_tower = first_tower.sort_values(by=['platformgameid', 'gametime'])
    first_tower["killerteamid_tower"] = first_tower["teamid"].apply(lambda x: 200 if x == 100 else 100)
    first_tower.drop_duplicates(subset=['platformgameid'], keep='first', inplace=True)
    first_tower.drop(columns=["buildingtype", "teamid"], inplace=True)

    first_inhib = first_inhib.merge(first_tower, on="platformgameid")

    print(first_inhib)

    event_start_times = pd.read_csv("csv/event_start_times.csv")
    event_start_times = event_start_times.sort_values(by=['platformgameid', 'eventtime'])

    df = first_inhib.merge(event_start_times, on="platformgameid")

    print(df)

    team_games = pd.read_csv("csv/team_games.csv")
    team_games.sort_values(by=['platformgameid'], inplace=True)

    with_teams = df.merge(team_games, on="platformgameid")

    blue_side = with_teams[with_teams["side"] == 100]
    blue_side.rename(columns={
        "teamid": "blue_teamid",
    }, inplace=True)
    blue_side.drop(columns=["gametime", "side"], inplace=True)
    red_side = with_teams[with_teams["side"] == 200]
    red_side.rename(columns={
        "teamid": "red_teamid",
    }, inplace=True)
    red_side.drop(columns=[
        "side",
        "esportsgameid",
        "gametime",
        "killerteamid_inhib",
        "eventtime",
    ], inplace=True)

    joined_side = blue_side.merge(red_side, on="platformgameid")
    
    
    print(joined_side)
    new_df = []

    LOOKBACK = 6
    team_stats = {}
    for _, row in joined_side.iterrows():
        if row["blue_teamid"] not in team_stats:
            team_stats[row["blue_teamid"]] = {
                "first_inhib": [0],
            }
        if row["red_teamid"] not in team_stats:
            team_stats[row["red_teamid"]] = {
                "first_inhib": [0],
            }

        
        new_df.append({
            "platformgameid": row["platformgameid"],
            "blue_teamid": row["blue_teamid"],
            "red_teamid": row["red_teamid"],
            "blue_avg_inhib": sum(team_stats[row["blue_teamid"]]["first_inhib"]) / len(team_stats[row["blue_teamid"]]["first_inhib"]),
            "red_avg_inhib": sum(team_stats[row["red_teamid"]]["first_inhib"]) / len(team_stats[row["red_teamid"]]["first_inhib"]),
        })

        if row["killerteamid_inhib"] == 100:
            team_stats[row["blue_teamid"]]["first_inhib"].append(1)
            team_stats[row["red_teamid"]]["first_inhib"].append(0)
        else:
            team_stats[row["blue_teamid"]]["first_inhib"].append(0)
            team_stats[row["red_teamid"]]["first_inhib"].append(1)

        if len(team_stats[row["blue_teamid"]]["first_inhib"]) > LOOKBACK:
            team_stats[row["blue_teamid"]]["first_inhib"].pop(0)
        if len(team_stats[row["red_teamid"]]["first_inhib"]) > LOOKBACK:
            team_stats[row["red_teamid"]]["first_inhib"].pop(0)
        
    
    new_df = pd.DataFrame(new_df)
    print(new_df)


roll_avg_first_tower()