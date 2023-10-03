import random
import logging
logging.basicConfig(filename="model_log.txt",
                    filemode='w',
                    # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

log = logging.getLogger('model')


class Team():
    def __init__(
        self,
        name,
    ):
        self.name = name
        self.kills = 0
        self.play_penalty = 0


class Model():
    def __init__(self):
        self.blue_team = Team("blue")
        self.red_team = Team("red")
        self.red_name = "red"
        self.red_kills = 0
        self.red_play_penalty = 0
        self.steps = 0
    
    def win(self):
        blue_win_roll = random.randint(0,100) - 30 + self.steps + self.blue_team.kills - self.red_kills
        red_win_roll = random.randint(0,100) - 30 + self.steps + self.red_kills - self.blue_team.kills
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
        kill_roll = round(random.random() + (random.random()*0.3 * (self.steps / 10)))
        if kill_roll > 5:
            kill_roll = 5
        if team == "blue":
            self.blue_team.kills += kill_roll
            log.info(f"blue team kill {self.blue_team.kills}|{self.red_kills}")

        elif team == "red":
            self.red_kills += kill_roll
            log.info(f"red team kill {self.blue_team.kills}|{self.red_kills}")

    def plays(self):
        """
        2. Both team roll for plays
        """
        blue_play_roll = random.randint(0,100) + self.blue_team.kills - self.red_kills
        if self.blue_team.play_penalty > 0:
            blue_play_roll -= 20
        red_play_roll = random.randint(0,100) + self.red_kills - self.blue_team.kills
        if self.red_play_penalty > 0:
            red_play_roll -= 20

        
        if blue_play_roll > 50:
            self.roll_for_kills(self.blue_team.name)
            self.blue_team.play_penalty = 2
        elif random.randint(0,100) > 70: # roll for counterplay
            self.roll_for_kills(self.red_name)
        if red_play_roll > 50:
            self.roll_for_kills(self.red_name)
            self.red_play_penalty = 2
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
        if self.red_play_penalty > 0:
            self.red_play_penalty -= 1
        
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
for i in range(300):
    model = Model()
    winners.append(model.run())


blue_win = [winner for winner in winners if winner == "blue"]
red_win = [winner for winner in winners if winner == "red"]
print(f"Blue wins {len(blue_win)}")
print(f"Red wins {len(red_win)}")
print(f"Blue win rate {len(blue_win)/len(winners)}")
print(f"Total {len(winners)}")
