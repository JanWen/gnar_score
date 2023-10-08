from chalicelib.esports import get_s3_file
import json



class Tournaments():
    def __init__(self):
        print("WARNING LOADING TOUNRAMNETS DATA (LARGE MEMORY FOOTPRINT)")
        json_data = get_s3_file("esports-data/tournaments")

        
        self.data = sorted(json.load(json_data), key=lambda item: item["startDate"])
    
    def yield_matches(self):
        for tournament in self.data: # Reverse order so we get the latest tournaments last
            for stage in tournament["stages"]:
                for section in stage["sections"]:
                    for match in section["matches"]:
                        if match["state"] == "completed":
                            yield tournament, match

    def yield_games(self):
        for tournament, league_id, match in self.yield_matches():
            for game in match["games"]:
                if game["state"] == "completed":
                    yield tournament, league_id, game