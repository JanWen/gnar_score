import json

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