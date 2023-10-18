import random
import logging
from chalicelib.models.team import Team, NoShutdownTeam
from chalicelib.models.logger import log
from chalicelib.elo import Elo
from chalicelib.models.logger import log



class EarlyGameTeam(Team):
    def __init__(self, name):
        super(EarlyGameTeam, self).__init__(name)
    def get_scaling_bonus(self, steps=None):
        # steps = float(steps)
        return -(0.3*steps)**2+3*steps-5


class LateGameTeam(Team):
    def __init__(self, name):
        super(LateGameTeam, self).__init__(name)
    def get_scaling_bonus(self, steps=None):
        return steps-10


class Match():
    def __init__(self, blue_team, red_team):
        self.blue_team = Team("blue")
        self.red_team = Team("red")
        self.steps = 0
        # self.blue_team.kills = 1
    
    def win(self):
        blue_win_roll = random.randint(0,100) - 30 + self.steps + self.blue_team.kills - self.red_team.kills
        red_win_roll = random.randint(0,100) - 30 + self.steps + self.red_team.kills - self.blue_team.kills
        if blue_win_roll > 100 and blue_win_roll > red_win_roll:
            log.info(f"Blue team wins")
            return "blue"
        if red_win_roll > 100 and red_win_roll > blue_win_roll:
            log.info(f"Red team wins")
            return "red"

    def plays(self):
        """
        2. Both team roll for plays
        """
        blue_play_roll = self.blue_team.roll_for_play(self.red_team, steps=self.steps)
        red_play_roll = self.red_team.roll_for_play(self.blue_team, steps=self.steps)
       
    
    def step(self):
        """
        1. Timestep for each minute
        """
        log.info(f"Step {self.steps}")
        
        self.plays()
        winner = self.win()
        if winner:
            log.info(f"Winner is {winner}")
            return winner
        
        if self.blue_team.play_penalty > 0:
            self.blue_team.play_penalty -= 1
        if self.red_team.play_penalty > 0:
            self.red_team.play_penalty -= 1
        
        self.steps += 1

    
    def run(self):
        """
        run the simulation
        """
        winner = None
        while not winner:
            winner = self.step()

        return winner


winners = []
blue_team = Team("blue")
red_team = Team("red")

team_ids = [
    Team("10"), 
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
]

elo = Elo(team_ids)
for i in range(1000):
    blue_id = random.choice(team_ids)
    red_id = random.choice(team_ids)
    model = Match(blue_team, red_team)
    winning_team = model.run()
    blue_team = {
        "id": blue_id,
        "result": {
            "outcome": "win" if winning_team == "blue" else "loss",
            "gameWins": 1 if winning_team == "blue" else 0,
        }
    }
    red_team = {
        "id": red_id,
        "result": {
            "outcome": "win" if winning_team == "red" else "loss",
            "gameWins": 1 if winning_team == "red" else 0,
        }
    }
    log.info("ELO_LOG: Elo before update")
    log.info(f"ELO_LOG: Blue team {blue_team} {elo.elo[blue_id].elo}")
    log.info(f"ELO_LOG: Red team {red_team} {elo.elo[red_id].elo}")

    elo.update_elo(blue_team, red_team, "league_id")

    log.info("ELO_LOG: Elo after update")
    log.info(f"ELO_LOG: Blue team {blue_team} {elo.elo[blue_id].elo}")
    log.info(f"ELO_LOG: Red team {red_team} {elo.elo[red_id].elo}")
    winners.append(winning_team)

blue_win = [winner for winner in winners if winner == "blue"]
red_win = [winner for winner in winners if winner == "red"]
print(f"Blue wins {len(blue_win)}")
print(f"Red wins {len(red_win)}")
print(f"Blue win rate {len(blue_win)/len(winners)}")
print(f"Total {len(winners)}")
