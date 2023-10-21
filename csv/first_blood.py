import pandas as pd


wins = pd.read_csv('csv/wins.csv')
wins = wins.sort_values(by=['platformgameid'])


"""
First Blood Stats
"""
def first_blood():

    print("First Blood Stats")
    first_kill = pd.read_csv("csv/first_blood.csv")
    first_kill = first_kill.sort_values(by=['platformgameid', 'gametime'])
    first_kill.drop_duplicates(subset=['platformgameid'], keep='first', inplace=True)
    first_blood = wins.merge(first_kill, on="platformgameid")
    print("Blue wins", len(first_blood[first_blood["winningteam"] == 100]))
    print("Red wins", len(first_blood[first_blood["winningteam"] == 200]))

    print("Blue first blood", len(first_blood[first_blood["killerteamid"] == 100]))
    print("Red first blood", len(first_blood[first_blood["killerteamid"] == 200]))
    print("Blue first blood win", len(first_blood[(first_blood["killerteamid"] == 100) & (first_blood["winningteam"] == 100)]))
    print("Red first blood win", len(first_blood[(first_blood["killerteamid"] == 200) & (first_blood["winningteam"] == 200)]))

    print("Blue first blood win rate", len(first_blood[(first_blood["killerteamid"] == 100) & (first_blood["winningteam"] == 100)])/len(first_blood[first_blood["killerteamid"] == 100]))
    print("Red first blood win rate", len(first_blood[(first_blood["killerteamid"] == 200) & (first_blood["winningteam"] == 200)])/len(first_blood[first_blood["killerteamid"] == 200]))
    print("Average game time", first_blood["gametime"].mean())

"""
Fist Tower Stats
"""
def first_tower():
    print("\nFist Tower Stats")
    first_building = pd.read_csv("csv/first_buildings.csv")
    first_tower = first_building[first_building["buildingtype"] == "turret"]
    first_tower = first_tower.sort_values(by=['platformgameid', 'gametime'])
    # teamid is the team that lost the tower
    first_tower["killerteamid"] = first_tower["teamid"].apply(lambda x: 200 if x == 100 else 100)
    first_tower.drop_duplicates(subset=['platformgameid'], keep='first', inplace=True)
    first_tower_blood = wins.merge(first_tower, on="platformgameid")

    print("Blue first tower", len(first_tower_blood[first_tower_blood["killerteamid"] == 100]))
    print("Red first tower", len(first_tower_blood[first_tower_blood["killerteamid"] == 200]))
    print("Blue first tower win", len(first_tower_blood[(first_tower_blood["killerteamid"] == 100) & (first_tower_blood["winningteam"] == 100)]))
    print("Red first tower win", len(first_tower_blood[(first_tower_blood["killerteamid"] == 200) & (first_tower_blood["winningteam"] == 200)]))
    print("Blue first tower win rate", len(first_tower_blood[(first_tower_blood["killerteamid"] == 100) & (first_tower_blood["winningteam"] == 100)])/len(first_tower_blood[first_tower_blood["killerteamid"] == 100]))
    print("Red first tower win rate", len(first_tower_blood[(first_tower_blood["killerteamid"] == 200) & (first_tower_blood["winningteam"] == 200)])/len(first_tower_blood[first_tower_blood["killerteamid"] == 200]))
    print("Average game time", first_tower_blood["gametime"].mean())


"""
Fist inhibitor Stats
"""
def first_inhibitor():
    print("\nFist Inhibitor Stats")
    first_building = pd.read_csv("csv/first_buildings.csv")
    first_inhib = first_building[first_building["buildingtype"] == "inhibitor"]
    first_inhib = first_inhib.sort_values(by=['platformgameid', 'gametime'])
    first_inhib["killerteamid"] = first_inhib["teamid"].apply(lambda x: 200 if x == 100 else 100)
    first_inhib.drop_duplicates(subset=['platformgameid'], keep='first', inplace=True)
    first_inhib_blood = wins.merge(first_inhib, on="platformgameid")
    print("Blue first inhib", len(first_inhib_blood[first_inhib_blood["killerteamid"] == 100]))
    print("Red first inhib", len(first_inhib_blood[first_inhib_blood["killerteamid"] == 200]))
    print("Blue first inhib win", len(first_inhib_blood[(first_inhib_blood["killerteamid"] == 100) & (first_inhib_blood["winningteam"] == 100)]))
    print("Red first inhib win", len(first_inhib_blood[(first_inhib_blood["killerteamid"] == 200) & (first_inhib_blood["winningteam"] == 200)]))
    print("Blue first inhib win rate", len(first_inhib_blood[(first_inhib_blood["killerteamid"] == 100) & (first_inhib_blood["winningteam"] == 100)])/len(first_inhib_blood[first_inhib_blood["killerteamid"] == 100]))
    print("Red first inhib win rate", len(first_inhib_blood[(first_inhib_blood["killerteamid"] == 200) & (first_inhib_blood["winningteam"] == 200)])/len(first_inhib_blood[first_inhib_blood["killerteamid"] == 200]))
    print("Average game time", first_inhib_blood["gametime"].mean())


first_blood()
first_tower()
first_inhibitor()
