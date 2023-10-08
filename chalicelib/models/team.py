import random
from chalicelib.models.logger import log

class Team():
    def __init__(
        self,
        name,
    ):
        self.name = name
        self.kills = 0
        self.play_penalty = 0

    def roll_for_play(self, opponent, steps=None):
        play_roll = random.randint(0,100) + self.get_scaling_bonus(steps) - opponent.kills + self.kills
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


class NoShutdownTeam(Team):
    def __init__(self, name):
        super(NoShutdownTeam, self).__init__(name)
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