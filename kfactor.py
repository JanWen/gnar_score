
from chalicelib.elo import calculate_elo
from chalicelib.tournaments import Tournaments
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import numpy as np

tournaments = Tournaments()


df = pd.read_csv("csv/sql/rolling.csv",
                dtype= {
                    'blue_teamid': 'str',
                    'red_teamid': 'str',
                })
df["eventtime"] = pd.to_datetime(df["eventtime"], errors="coerce")
df["blue_teamid"].fillna(0, inplace=True)
df["red_teamid"].fillna(0, inplace=True)
df["blue_teamid"] = df["blue_teamid"].astype(np.int64).astype(str)
df["red_teamid"] = df["red_teamid"].astype(np.int64).astype(str)
x = df[[
        "blue_avg_inhib", "red_avg_inhib",
        "blue_avg_tower", "red_avg_tower",
        "blue_avg_kills", "red_avg_kills",
        "blue_avg_win", "red_avg_win",
        "red_avg_deaths", "blue_avg_deaths",
        "blue_level", "red_level",
        "blue_cs", "red_cs",
        "blue_avg_kill", "red_avg_kill",
]]
y = df["winningteam"]
gnb = GaussianNB()
model = gnb.fit(x, y)


errors = []
for i in range(10, 100, 5):
    K_FACTOR = i
    elo, back_test, mean_sq_er = calculate_elo(tournaments, k_factor=K_FACTOR, df=df, model=model)
    errors.append((K_FACTOR, mean_sq_er))
    # print(elo)

sorted_errors = sorted(errors, key=lambda x: x[1])
for i,j in sorted_errors[:5]:
    print(i, round(j, 3))