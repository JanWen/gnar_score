import pandas as pd

wins = pd.read_csv('csv/wins.csv')

blue_wins = wins[wins["winningteam"] == 100]
red_wins = wins[wins["winningteam"] == 200]

print("Total wins", len(wins))
print("Blue wins", len(blue_wins))
print("Red wins", len(red_wins))

print("Blue win rate", len(blue_wins)/len(wins))