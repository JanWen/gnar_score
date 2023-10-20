import random
import logging
# from chalicelib.models.team import Team, NoShutdownTeam
from chalicelib.team import Team
from chalicelib.models.logger import log
from chalicelib.elo import Elo
from chalicelib.models.logger import log



class EarlyGameTeam(Team):
    def __init__(self, name):
        self.type = "EarlyGameTeam"
        super(EarlyGameTeam, self).__init__(name)
    def get_scaling_bonus(self, steps=None):
        # steps = float(steps)
        return -(0.3*steps)**2+3*steps-5


class LateGameTeam(Team):
    def __init__(self, name):
        self.type = "LateGameTeam"
        super(LateGameTeam, self).__init__(name)
    def get_scaling_bonus(self, steps=None):
        return steps-10


class Match():
    def __init__(self, blue_team, red_team):
        self.blue_team = blue_team
        self.red_team = red_team
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
        1. Time step for each minute
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

teams = [
    EarlyGameTeam(("11", 1000)),
    EarlyGameTeam(("12", 1000)),
    EarlyGameTeam(("13", 1000)),
    EarlyGameTeam(("14", 1000)),
    EarlyGameTeam(("15", 1000)),
    LateGameTeam(("16", 1000)),
    LateGameTeam(("17", 1000)),
    LateGameTeam(("18", 1000)),
    LateGameTeam(("19", 1000)),
    LateGameTeam(("20", 1000)),
]
winners_teams = {
    team.id: 0 for team in teams
}
matches_teams = {
    team.id: 0 for team in teams
}

elo = Elo(teams)
for i in range(1000):
    blue_team = random.choice(teams)
    red_team = random.choice(teams)
    while red_team.id == blue_team.id:
        red_team = random.choice(teams)
    blue_id = blue_team.id
    red_id = red_team.id
    model = Match(blue_team, red_team)
    winning_team = model.run()
    blue_team_outcome = {
        "id": blue_id,
        "result": {
            "outcome": "win" if winning_team == "blue" else "loss",
            "gameWins": 1 if winning_team == "blue" else 0,
        }
    }
    red_team_outcome = {
        "id": red_id,
        "result": {
            "outcome": "win" if winning_team == "red" else "loss",
            "gameWins": 1 if winning_team == "red" else 0,
        }
    }
    log.info("ELO_LOG: Elo before update")
    log.info(f"ELO_LOG: Blue team {blue_team.name} {elo.elo[blue_id].elo}")
    log.info(f"ELO_LOG: Red team {red_team.name} {elo.elo[red_id].elo}")

    elo.update_elo(blue_team_outcome, red_team_outcome, "league_id")

    log.info("ELO_LOG: Elo after update")
    log.info(f"ELO_LOG: Blue team {blue_team.name} {elo.elo[blue_id].elo}")
    log.info(f"ELO_LOG: Red team {red_team.name} {elo.elo[red_id].elo}")
    if winning_team == "blue":
        winners_teams[blue_id] += 1
    if winning_team == "red":
        winners_teams[red_id] += 1

    blue_team.reset_stats()
    red_team.reset_stats()
    winners.append(winning_team)
    matches_teams[blue_id] += 1
    matches_teams[red_id] += 1

blue_win = [winner for winner in winners if winner == "blue"]
red_win = [winner for winner in winners if winner == "red"]
print(f"Blue wins {len(blue_win)}")
print(f"Red wins {len(red_win)}")
print(f"Blue win rate {len(blue_win)/len(winners)}")
print(f"Total {len(winners)}")

for i,j in elo.elo.items():
    print(i,j.elo)

# for i,j in winners_teams.items():
#     print(i,j)

# for i,j in matches_teams.items():
#     print(i,j)