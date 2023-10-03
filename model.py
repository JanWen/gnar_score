import random
import logging
from src.models.team import Team
from src.models.logger import log


class EarlyGameTeam(Team):
    def __init__(self, name):
        super(EarlyGameTeam, self).__init__(name)
        self.scaling_var = 20
        self.scaling_var += 1
    def get_scaling_bonus(self):
        self.scaling_var -= 1
        return self.scaling_var


class LateGameTeam(Team):
    def __init__(self, name):
        super(LateGameTeam, self).__init__(name)
        self.scaling_var = -10
        self.scaling_var -= 1
    def get_scaling_bonus(self):
        self.scaling_var += 1
        return self.scaling_var

class Model():
    def __init__(self):
        self.blue_team = Team("blue")
        self.red_team = Team("red")
        self.steps = 0
    
    def win(self):
        blue_win_roll = random.randint(0,100) - 30 + self.steps + self.blue_team.kills - self.red_team.kills
        red_win_roll = random.randint(0,100) - 30 + self.steps + self.red_team.kills - self.blue_team.kills
        if blue_win_roll > 100:
            log.info(f"Blue team wins")
            return "blue"
        if red_win_roll > 100:
            log.info(f"Red team wins")
            return "red"

    def roll_for_kills(self, team):
        """
        3. Team that makes play rolls for kills
        
        """
        kill_roll = round(random.random())
        #skirmush_bonus
        if round(random.random()*0.3):
            kill_roll += round(random.random()*(self.steps / 10))
        if kill_roll > 5:
            kill_roll = 5
        if team == "blue":
            self.blue_team.kills += kill_roll
            log.info(f"blue team kill {self.blue_team.kills}|{self.red_team.kills}")

        elif team == "red":
            self.red_team.kills += kill_roll
            log.info(f"red team kill {self.blue_team.kills}|{self.red_team.kills}")

    def plays(self):
        """
        2. Both team roll for plays
        """
        blue_play_roll = self.blue_team.roll_for_play(self.red_team)
        red_play_roll = self.red_team.roll_for_play(self.blue_team)

        
        if blue_play_roll > 50:
            self.blue_team.roll_for_kills(self.red_team)
            self.blue_team.play_penalty = 2
        elif random.randint(0,100) > 70: # roll for counterplay
            self.red_team.roll_for_kills(self.blue_team)
        if red_play_roll > 50:
            self.red_team.roll_for_kills(self.blue_team)
            self.red_team.play_penalty = 2
        elif random.randint(0,100) > 70: # roll for counterplay
            self.roll_for_kills(self.blue_team.name)

    
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
for i in range(1000):
    model = Model()
    winners.append(model.run())


blue_win = [winner for winner in winners if winner == "blue"]
red_win = [winner for winner in winners if winner == "red"]
print(f"Blue wins {len(blue_win)}")
print(f"Red wins {len(red_win)}")
print(f"Blue win rate {len(blue_win)/len(winners)}")
print(f"Total {len(winners)}")
