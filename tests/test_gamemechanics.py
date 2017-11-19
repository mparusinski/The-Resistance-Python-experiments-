import unittest
from gamemechanics import *
from Player import ProxiedPlayer

def generateProxiedPlayers():
    players = list(map(lambda x: ProxiedPlayer("Player " + str(x + 1)), range(5)))
    return players

class TestGameState(unittest.TestCase):

    def test_get_current_leader(self):
        players = generateProxiedPlayers()
        game_state = GameState(players)
        current_leader = game_state.get_current_leader()
        self.assertEqual(current_leader, players[0])


if __name__ == "__main__":
    unittest.main()
