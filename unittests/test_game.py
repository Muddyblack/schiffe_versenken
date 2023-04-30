# pylint: disable=C)
import unittest
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

from classes.game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_get_save_path(self):
        self.assertEqual(self.game.get_save_path(), ) #...

    def test_get_players(self):
        self.assertEqual(self.game.get_players(), ["Player"])

    def test_get_current_level(self):
        self.assertEqual(self.game.get_current_level(), "0")  # 1?

    def test_get_last_turn_player(self):
        self.assertEqual(self.game.get_last_turn_player(), "Player")

    def test_set_players(self):
        players = {"Lena", "Lara"}
        self.game.set_players(players)
        self.assertEqual(self.game.get_players(), {"Lena", "Lara"})

    def test_set_current_level(self):
        level = 1
        self.game.set_current_level(level)
        self.assertEqual(self.game.get_current_level(), level)  # oder anstatt level 1

    def test_set_last_turn_player(self):
        player_last_turn = "Lena"
        self.game.set_last_turn_player(player_last_turn)
        self.assertEqual(self.game.get_last_turn_player, "Lena")  # oder Lena


if __name__ == "__main__":
    unittest.main()
