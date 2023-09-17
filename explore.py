import json

def tournaments():
    tournaments_data = json.load(open("esports-data/tournaments.json", "r"))

    print("Tournaments:" + str(len(tournaments_data)))

    stages = 0
    matches = 0

    for tournament in tournaments_data:
        print(tournament["name"])
        stages += len(tournament["stages"])
        for stage in tournament["stages"]:
            for section in stage["sections"]:
                matches += len(section["matches"])

    print("Stages:" + str(stages))
    print("Matches:" + str(matches))

def elo_form(x,y):
    ea = 1/(1+10**((y-x)/400))
    eb = 1/(1+10**((x-y)/400))

    ra = x + 32*(1-ea)
    return ra


