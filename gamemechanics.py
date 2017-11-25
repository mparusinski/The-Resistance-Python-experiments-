import random
from player import MonkeyPlayer

PLAYERS_PER_MISSION = [2, 3, 2, 3, 3]

def default_spy_selection_process():
    randomGen = random.Random(0)
    return randomGen.sample(range(5), 2)

# Represent a game at a given step
class GameState(object): # or start

    def __init__(self, players):
        self.spy_successes = 0
        self.loyal_successes = 0
        self.cumulated_rejections = 0
        self.current_mission = 0
        self.players = players
        self.current_leader_pos = 0
        self.spy_victory = False
        self.loyal_victory = False
        self.spies = []
        self.verbose = False
        self.spy_selection_process = default_spy_selection_process

    def next_state(self):
        return SpiesSelection(self)

    def get_current_leader(self):
        return self.players[self.current_leader_pos]

    def next_leader(self):
        self.current_leader_pos = (self.current_leader_pos + 1) % len(self.players)

    def game_ended(self):
        return self.spy_victory or self.loyal_victory

    def is_spy_victory(self):
        return self.spy_victory

    def is_loyal_victory(self):
        return self.loyal_victory

    def set_verbose(self, verbosity):
        self.verbose = verbosity

    def nextMission(self):
        self.current_mission = self.current_mission + 1

    def log_message(self, message):
        if self.verbose:
            print(message)
        
    def set_spy_selection_process(self, spy_selection_func):
        self.spy_selection_process = spy_selection_func


class SpiesSelection(GameState):

    def __init__(self, previous):
        self.__dict__ = dict(previous.__dict__)
        self.spies = self.spy_selection_process()
        for i in self.spies:
            self.log_message("Player " + str(i + 1) + " is a spy")
            self.players[i].assign_spy_role(self.spies)

    def next_state(self):
        return MissionSelection(self)



class MissionSelection(GameState):

    def __init__(self, previous):
        self.__dict__ = dict(previous.__dict__)

    def next_state(self):
        current_leader = self.get_current_leader()
        mission = current_leader.select_mission(self.players, PLAYERS_PER_MISSION[self.current_mission])
        ret_str = "In mission"
        for player in mission:
            ret_str = ret_str + " " + player.get_player_name()
        self.log_message(ret_str)
        return MissionProposal(self, mission)


class MissionProposal(GameState):

    def __init__(self, previous, mission):
        self.__dict__ = dict(previous.__dict__)
        self.mission = mission

    def next_state(self):
        favor = 0
        oppose = 0
        for player in self.players:
            vote = player.vote_on_mission(self.mission)
            if vote:
                favor = favor + 1
            else:
                oppose = oppose + 1
        if favor > oppose:
            self.log_message("Mission was accepted")
            return MissionExecution(self, self.mission)
        else:
            self.log_message("Mission was opposed")
            self.cumulated_rejections = self.cumulated_rejections + 1
            if self.cumulated_rejections > 5:
                self.log_message("Spies won through 5 repeated rejections")
                return SpyVictory(self)
            self.next_leader()
            return MissionSelection(self)


class MissionExecution(GameState):

    def __init__(self, previous, mission):
        self.__dict__ = dict(previous.__dict__)
        self.mission = mission

    def next_state(self):
        failure = False
        for player in self.mission:
            if player.is_spy() and player.sabotage_mission():
                failure = True
        if failure:
            self.log_message("Mission was sabotaged")
            self.spy_successes = self.spy_successes + 1
        else:
            self.log_message("Mission was carried out successfully")
            self.loyal_successes = self.loyal_successes + 1
        if self.spy_successes > 2:
            self.log_message("Spies won through 3 successfully sabotaged missions")
            return SpyVictory(self)
        elif self.loyal_successes > 2:
            self.log_message("Loyal won through 3 successfully carried out missions")
            return LoyalVictory(self)
        self.next_leader()
        self.nextMission()
        return MissionSelection(self)

class SpyVictory(GameState):

    def __init__(self, previous):
        self.__dict__ = dict(previous.__dict__)
        self.spy_victory = True


class LoyalVictory(GameState):

    def __init__(self, previous):
        self.__dict__ = dict(previous.__dict__)
        self.loyal_victory = True


def run_game():
    players = []
    for i in range(5):
        players.append(MonkeyPlayer("Player " + str(i)))
    spy_vict = 0
    for i in range(100):
        a_game = GameState(players)
        a_game.set_verbose(False)
        while not a_game.game_ended():
            a_game = a_game.next_state()
        if a_game.is_spy_victory():
            spy_vict = spy_vict + 1
    print("Out of 100 games, spies won " + str(spy_vict) + " times")

def main():
    run_game()

if __name__ == '__main__':
    main()