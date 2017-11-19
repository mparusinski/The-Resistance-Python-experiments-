import random
from functools import reduce

class Player(object): # Abstract / Dumb Player

    def __init__(self, playerName):
        self.spyRole = False
        self.playerName = playerName
        self.otherSpies = None

    def assignSpyRole(self, otherSpies):
        self.otherSpies = otherSpies
        self.spyRole = True

    def selectMission(self, players, numOfPlayersRequired):
        return players[0:numOfPlayersRequired]

    def voteOnMission(self, mission):
        return True

    def sabotageMission(self):
        return True

    def getPlayerName(self):
        return self.playerName

    def isSpy(self):
        return self.spyRole


class ProxiedPlayer(Player):

    def __init__(self, playerName):
        Player.__init__(self, playerName)
        self.proxy_select_mission = None
        self.proxy_vote_on_mission = None
        self.proxy_sabotage_mission = None

    def set_proxy_select_mission(self, proxy_func):
        self.proxy_select_mission = proxy_func

    def set_proxy_vote_on_mission(self, proxy_func):
        self.proxy_vote_on_mission = proxy_func

    def set_proxy_sabotage_mission(self, proxy_func):
        self.proxy_sabotage_mission = proxy_func

    def selectMission(self, players, numOfPlayersRequired):
        return self.proxy_select_mission(players, numOfPlayersRequired)

    def voteOnMission(self, mission):
        return self.proxy_vote_on_mission(mission)

    def sabotageMission(self):
        return self.proxy_sabotage_mission()


class MonkeyPlayer(Player):

    def __init__(self, playerName):
        Player.__init__(self, playerName)

    def selectMission(self, players, numOfPlayersRequired):
        indexes = random.sample(range(5), numOfPlayersRequired)
        mission = []
        for i in indexes:
            mission.append(players[i])
        return mission

    def voteOnMission(self, mission):
        anInt = random.randint(0,1)
        if anInt == 0:
            return False
        else:
            return True

    def sabotageMission(self):
        anInt = random.randint(0,1)
        if anInt == 0:
            return False
        else:
            return True


class HumanConsoleUIPlayer(Player):

    def __init__(self, playerName):
        Player.__init__(self, playerName)

    def assignSpyRole(self, otherSpies):
        self.otherSpies = otherSpies
        self.spyRole = True
        print("You are a spy")
        print("The list of spies is " + reduce(lambda x, y: str(x.getPlayerName()) + " " + str(y.getPlayerName()), otherSpies))

    def selectMission(self, players, numOfPlayersRequired):
        print("For this mission " + str(numOfPlayersRequired) + " of players are required!")
        print("Whom do you choose?")
        mission = []
        while len(mission) < numOfPlayersRequired:
            selectionStr = input("Type a number between 1 and 5: ")
            selection = int(selectionStr)
            if selection in mission:
                print("You already choose this player, please choose someone else")
            mission.append(selection)
        return mission

    def voteOnMission(self, mission):
        print("In the mission you will find players " + reduce(lambda x, y: str(x.getPlayerName()) + " " + str(y.getPlayerName()), mission))
        noAnswer = True
        while noAnswer:
            approval = input("Do you approve (Y/N)? ")
            if approval == "Y":
                return True
            elif approval == "N":
                return False
            else:
                print("Invalid input")

    def sabotageMission(self):
        print("As a spy you can sabotage the mission")
        noAnswer = True
        while noAnswer:
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