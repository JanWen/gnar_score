import random
from src.models.logger import log

class Team():
    def __init__(
        self,
        name,
    ):
        self.name = name
        self.kills = 0
        self.play_penalty = 0

    def roll_for_play(self, opponent):
        play_roll = random.randint(0,100) + self.get_scaling_bonus() - opponent.kills + self.kills
        if self.play_penalty > 0:
            play_roll -= 20
        # if play_roll > 50:
        #     self.
        return play_roll
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
        self.kills += kill_roll
        log.info(f"{self.name} team kill {self.kills}|{opponent.kills}")


    
    def get_scaling_bonus(self):
        return 0