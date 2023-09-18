from src.esports import teams_data
from src.leagues import get_league_name, get_league_elo_ratio
class Team:
    def __init__(self, elo_tuple):
        self.id = elo_tuple[0]
        self.elo = elo_tuple[1]
        self.games = 0
        self.matches = 0
        self.rank = 0
        self.leagues = []
        self.team_info = [team for team in teams_data if team["team_id"] == self.id]
        if len(self.team_info):
            self.team_name = self.team_info[0]["name"]
            self.code = self.team_info[0]["acronym"]
        else:
            self.team_name = "UNKNOWN"
            self.code = "UNKNOWN"

    

    def adjusted_elo(self):
        main_league = self.get_main_league()
        league_name = get_league_name(main_league)
        return self.elo * get_league_elo_ratio(league_name)

    def json(self):
        main_league = self.get_main_league()
        league_name = get_league_name(main_league)
        return {
                "team_id": self.id,
                "team_code": self.code,
                "team_name": self.team_name,
                "rank": self.rank,
                "matches": self.matches,
                "elo": round(self.elo) *  get_league_elo_ratio(league_name),
                # "elo_ratio":,
                "league": league_name,
            }
    
    def get_main_league(self):
        if len(self.leagues) == 0:
            return "UNKNOWN"
        return max(set(self.leagues), key = self.leagues.count)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return f"{self.team_name} {self.elo} {self.games} {self.get_main_league()}"