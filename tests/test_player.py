import unittest
from player import *

class TestAbstractPlayer(unittest.TestCase):

    def test_player_is_abstract(self):
        with self.assertRaises(TypeError):
            an_dummy_player = AbstractPlayer("AnHackerPlayer")


class TestProxiedPlayer(unittest.TestCase):

    def test_proxied_player_select_mission(self):
        a_player = ProxiedPlayer("ProxiedPlayer")
        self.assertEqual(a_player.get_player_name(), "ProxiedPlayer")
        a_player.set_proxy_select_mission(lambda mission, num : mission[0:num])
        self.assertEqual(a_player.select_mission(list(range(5)), 2), [0,1])

    def test_proxied_player_vote_on_mission(self):
        a_player = ProxiedPlayer("ProxiedPlayer")
        self.assertEqual(a_player.get_player_name(), "ProxiedPlayer")
        a_player.set_proxy_vote_on_mission(lambda mission: False)
        a_mission = list(map(lambda x : ProxiedPlayer("Player " + str(x)), range(2)))
        self.assertEqual(a_player.vote_on_mission(a_mission), False)

    def test_proxied_player_sabotage_mission(self):
        a_player = ProxiedPlayer("ProxiedPlayer")
        self.assertEqual(a_player.get_player_name(), "ProxiedPlayer")
        a_player.set_proxy_sabotage_mission(lambda: True)
        self.assertEqual(a_player.sabotage_mission(), True)


class TestMonkeyPlayer(unittest.TestCase):

    def test_monkey_player(self):
        monkeys = list(map(lambda x: MonkeyPlayer("A Monkey Player"), range(5)))
        monkey = monkeys[0]
        self.assertEqual(monkey.get_player_name(), "A Monkey Player")
        self.assertEqual(len(monkey.select_mission(monkeys, 2)), 2)
        self.assertEqual(len(monkey.select_mission(monkeys, 3)), 3)


if __name__ == "__main__":
    unittest.main()