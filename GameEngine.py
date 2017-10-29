# Mission = [Players]
# 
# GameStep = MissionSelection
#          | MissionProposal Mission
#          | MissionExecution Mission
#		   | SpyVictory | LoyalVictory

import copy
import random

numOfPlayersPerMission = [2,3,2,3,3]

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
		if self.spyRole:
			return True
		else:
			return False

	def getPlayerName(self):
		return self.playerName


# Represent a game at a given step
class GameStep(object): # or start

	def __init__(self, players):
		self.spy_successes = 0
		self.loyal_successes = 0
		self.cumulated_rejections = 0
		self.currentMission = 0
		self.players = players
		self.current_leader_pos = 0
		self.num_of_players = len(players)
		self.spy_victory = False
		self.loyal_victory = False
		self.spies = []

	def nextStep(self):
		return SpiesSelection(self)

	def getCurrentLeader(self):
		return self.players[self.current_leader_pos]

	def nextLeader(self):
		self.current_leader_pos = self.current_leader_pos + 1 % self.num_of_players

	def gameEnded(self):
		return self.spy_victory or self.loyal_victory


class SpiesSelection(GameStep):

	def __init__(self, previous):
		self.__dict__ = dict(previous.__dict__)
		self.spies = random.sample(range(5), 2)
		for i in self.spies:
			print("Player " + str(i + 1) + " is a spy")
			self.players[i].assignSpyRole(self.spies)

	def nextStep(self):
		return MissionSelection(self)



class MissionSelection(GameStep):

	def __init__(self, previous):
		self.__dict__ = dict(previous.__dict__)
		self.currentMission = self.currentMission + 1

	def nextStep(self):
		currentLeader = self.getCurrentLeader()
		mission = currentLeader.selectMission(self.players, numOfPlayersPerMission[self.currentMission - 1])
		retStr = "In mission"
		for player in mission:
			retStr = retStr + " " + player.getPlayerName()
		print(retStr)
		return MissionProposal(self, mission)


class MissionProposal(GameStep):

	def __init__(self, previous, mission):
		self.__dict__ = dict(previous.__dict__)
		self.mission = mission

	def nextStep(self):
		favor = 0
		oppose = 0
		for player in self.players:
			vote = player.voteOnMission(self.mission)
			if vote:
				favor = favor + 1
			else:
				oppose = oppose + 1
		if favor > oppose:
			print("Mission was accepted")
			return MissionExecution(self, self.mission)
		else:
			print("Mission was opposed")
			self.cumulated_rejections = self.cumulated_rejections + 1
			if self.cumulated_rejections > 5:
				print("Spies won through 5 repeated rejections")
				return SpyVictory(self)
			self.nextLeader()
			return MissionProposal(self)


class MissionExecution(GameStep):

	def __init__(self, previous, mission):
		self.__dict__ = dict(previous.__dict__)
		self.mission = mission

	def nextStep(self):
		failure = False
		for player in self.mission:
			if player.sabotageMission():
				failure = True
		if failure:
			print("Mission was sabotaged")
			self.spy_successes = self.spy_successes + 1
		else:
			print("Mission was carried out successfully")
			self.loyal_successes = self.loyal_successes + 1
		if self.spy_successes > 2:
			print("Spies won through 3 successfully sabotaged missions")
			return SpyVictory(self)
		elif self.loyal_successes > 2:
			print("Loyal won through 3 successfully carried out missions")
			return LoyalVictory(self)
		self.nextLeader()
		return MissionSelection(self)

class SpyVictory(GameStep):

	def __init__(self, previous):
		self.__dict__ = dict(previous.__dict__)
		self.spy_victory = True


class LoyalVictory(GameStep):

	def __init__(self, previous):
		self.__dict__ = dict(previous.__dict__)
		self.loyal_victory = True


def runGame():
	players = []
	for i in range(5):
		players.append(Player("Player " + str(i + 1)))
	aGame = GameStep(players)
	while not aGame.gameEnded():
		aGame = aGame.nextStep()

def main():
	runGame()

if __name__ == '__main__':
	main()