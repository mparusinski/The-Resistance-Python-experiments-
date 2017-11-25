import random
from abc import ABC, abstractmethod
from functools import reduce

class AbstractPlayer(ABC): # Abstract / Dumb Player

    def __init__(self, player_name):
        self.spy_role = False
        self.player_name = player_name
        self.other_spies = None

    def assign_spy_role(self, other_spies):
        self.other_spies = other_spies
        self.spy_role = True

    @abstractmethod
    def select_mission(self, players, num_players_required):
        pass

    @abstractmethod
    def vote_on_mission(self, mission):
        pass

    @abstractmethod
    def sabotage_mission(self):
        pass

    def get_player_name(self):
        return self.player_name

    def is_spy(self):
        return self.spy_role


class ProxiedPlayer(AbstractPlayer):

    def __init__(self, playerName):
        AbstractPlayer.__init__(self, playerName)
        self.proxy_select_mission = None
        self.proxy_vote_on_mission = None
        self.proxy_sabotage_mission = None

    def set_proxy_select_mission(self, proxy_func):
        self.proxy_select_mission = proxy_func

    def set_proxy_vote_on_mission(self, proxy_func):
        self.proxy_vote_on_mission = proxy_func

    def set_proxy_sabotage_mission(self, proxy_func):
        self.proxy_sabotage_mission = proxy_func

    def select_mission(self, players, num_players_required):
        return self.proxy_select_mission(players, num_players_required)

    def vote_on_mission(self, mission):
        return self.proxy_vote_on_mission(mission)

    def sabotage_mission(self):
        return self.proxy_sabotage_mission()


class MonkeyPlayer(AbstractPlayer):

    def __init__(self, playerName):
        AbstractPlayer.__init__(self, playerName)

    def select_mission(self, players, num_players_required):
        indexes = random.sample(range(5), num_players_required)
        mission = []
        for i in indexes:
            mission.append(players[i])
        return mission

    def vote_on_mission(self, mission):
        anInt = random.randint(0,1)
        if anInt == 0:
            return False
        else:
            return True

    def sabotage_mission(self):
        anInt = random.randint(0,1)
        if anInt == 0:
            return False
        else:
            return True


class HumanConsoleUIPlayer(AbstractPlayer):

    def __init__(self, playerName):
        AbstractPlayer.__init__(self, playerName)

    def assign_spy_role(self, other_spies):
        self.otherSpies = otherSpies
        self.spyRole = True
        print("You are a spy")
        print("The list of spies is " + reduce(lambda x, y: str(x.getPlayerName()) + " " + str(y.getPlayerName()), otherSpies))

    def select_mission(self, players, num_players_required):
        print("For this mission " + str(num_players_required) + " of players are required!")
        print("Whom do you choose?")
        mission = []
        while len(mission) < num_players_required:
            selection_str = input("Type a number between 1 and 5: ")
            selection = int(selection_str)
            if selection in mission:
                print("You already choose this player, please choose someone else")
            mission.append(selection)
        return mission

    def vote_on_mission(self, mission):
        print("In the mission you will find players " + reduce(lambda x, y: str(x.get_player_name()) + " " + str(y.get_player_name()), mission))
        no_answer = True
        while no_answer:
            approval = input("Do you approve (Y/N)? ")
            if approval == "Y":
                return True
            elif approval == "N":
                return False
            else:
                print("Invalid input")

    def sabotage_mission(self):
        print("As a spy you can sabotage the mission")
        no_answer = True
        while no_answer:
            approval = input("Do you sabotage the mission (Y/N)? ")
            if approval == "Y":
                return True
            elif approval == "N":
                return False
            else:
                print("Invalid input")


def main():
    pass

if __name__ == "__main__":
    main()