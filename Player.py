import random

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


def main():
	pass

if __name__ == "__main__":
	main()