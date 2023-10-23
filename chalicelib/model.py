from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

def load_model(features=None):
    default_features = [
        # "first_blood_avg",
        "first_inhibitor_avg",
        "first_tower_avg",
        "kills_avg",
        "win_avg",
        "deaths_avg",
        # "level_avg",
        "cs_avg",
    ]
    if not features:
        features = default_features
    print("Loading model")
    df = pd.read_csv("csv/sql/processed.csv", dtype= {'teamid': 'str'})
    blue_side = df[df["side"] == 100]
    blue_side = blue_side.rename(columns={
        "teamid": "blue_teamid",
    })
    blue_side.drop(columns=["side"], inplace=True)

    red_side = df[df["side"] == 200]
    red_side = red_side.rename(columns={
        "teamid": "red_teamid",
    })
    red_side.drop(columns=["side", "esportsgameid"], inplace=True)

    df = blue_side.merge(red_side, on="platformgameid", suffixes=("_blue", "_red"))
    df['winningteam'] = np.where(df['win_blue'] == 1, 100, 200)
    df.drop(columns=["win_blue", "win_red"], inplace=True)

    df.fillna(0, inplace=True)
    features = [i+"_blue" for i in features] + [i+"_red" for i in features ]
    X = df[features]
    y = df["winningteam"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    gnb = GaussianNB()
    model = gnb.fit(X_train,y_train)
    predictive_labels = gnb.predict(X_test)
    print("Accuracy score:", round(accuracy_score(y_test, predictive_labels), 3))
    return df, features, model