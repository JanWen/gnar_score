from src.esports import teams_data

class Team:
    def __init__(self, elo_tuple):
        self.id = elo_tuple[0]
        self.elo = elo_tuple[1]
        self.games = 0
        self.rank = 0
        self.team_info = [team for team in teams_data if team["team_id"] == self.id]
        if len(self.team_info):
            self.team_name = self.team_info[0]["name"]
            self.code = self.team_info[0]["acronym"]
        else:
            self.team_name = "UNKNOWN"
            self.code = "UNKNOWN"

    def json(self):
        return {
                "team_id": self.id,
                "team_code": self.code,
                "team_name": self.team_name,
                "rank": self.rank,
                "elo": round(self.elo),
            }
    
    
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return "%s %s %s" % (self.team_name, self.elo, self.games)