from chalicelib.esports import teams_data
from chalicelib.leagues import get_league_name, get_league_elo_ratio
import random
from chalicelib.models.logger import log

class Team:
    def __init__(self, elo_tuple):
        self.id = elo_tuple[0]
        self.name = self.id
        self.elo = elo_tuple[1]
        self.matches = 0
        self.rank = 0
        self.leagues = []
        self.kills = 0
        self.play_penalty = 0
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
        elo_ratio = get_league_elo_ratio(league_name)
        elo = round(self.elo * elo_ratio)
        if elo_ratio == 0 or elo == 0:
            print(f"WARNING: {self.team_name} has no elo ratio for {league_name}")
        return {
                "team_id": self.id,
                "team_code": self.code,
                "team_name": self.team_name,
                "rank": self.rank,
                "matches": self.matches,
                "elo": elo,
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
        return f"{self.team_name} {self.elo} {self.matches} {self.get_main_league()}"
    


    # fucntions for model
    def roll_for_play(self, opponent, steps=None):
        bonus = self.get_scaling_bonus(steps)
        play_roll = random.randint(0,100) + bonus - opponent.kills + self.kills
        if self.play_penalty > 0:
            play_roll -= 20

        if play_roll > 50:
            self.roll_for_kills(opponent)
            self.play_penalty = 2
        elif random.randint(0,100) > 70: # roll for counterplay
            opponent.roll_for_kills(self)


    def roll_for_kills(self, opponent):
        """
        3. Team that makes play rolls for kills
        
        """
        kill_roll = round(random.random())
        #skirmush_bonus
        if round(random.random()*0.3):
            kill_roll += round(random.random()*(self.steps / 10))
        if kill_roll > 5:
            kill_roll = 5
        #shutdown bonus
        if opponent.kills - self.kills > 3:
            kill_roll += round((opponent.kills - self.kills)/3)
        self.kills += kill_roll
        log.info(f"{self.name} team kill {self.kills}|{opponent.kills}")


    def get_scaling_bonus(self, steps=None):
        return 0
