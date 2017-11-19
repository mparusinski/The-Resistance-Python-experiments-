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

    def test_direct_spy_win_game(self):
        players = generateProxiedPlayers()
        game_state = GameState(players)
        game_state.set_spy_selection_process(lambda : [0,1])
        for player in players:
            player.set_proxy_select_mission(lambda players, num: players[0:num])
            player.set_proxy_vote_on_mission(lambda x: True)
            player.set_proxy_sabotage_mission(lambda: True)
        while not game_state.game_ended():
            game_state = game_state.next_state()
        self.assertTrue(game_state.is_spy_victory())
        self.assertFalse(game_state.is_loyal_victory())
        self.assertEqual(game_state.loyal_successes, 0)
        self.assertEqual(game_state.spy_successes, 3)
        self.assertEqual(game_state.cumulated_rejections, 0)


if __name__ == "__main__":
    unittest.main()
