# pylint: disable=C
import sys
import os
import unittest
from unittest import mock
import io
import sys
import re
import os
from unittest.mock import patch


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

from classes.player import Player
from classes.game_field import GameField
from classes.game import Game

from main import left_to_place_ships, place_all_ships, attack_execution


ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def set_testing_ship(field, start_row, start_column, shiplen, shiptype, direction):
    with patch.object(
        GameField,
        "_GameField__get_row_and_column_input",
        return_value=(start_row, start_column),
    ):
        with patch(
            "keyboard.is_pressed",
            side_effect=lambda key: key == direction,
        ):
            field.set_ship(ship_len=shiplen, ship_type=shiptype, is_bot=False)


class TestGameFuncs(unittest.TestCase):
    def setUp(self):
        self.ship_types = {
            "battleship": {"max": "1", "length": "5"},
            "destroyer": {"max": "1", "length": "3"},
        }

        self.game = Game()
        self.player1 = Player(name="Player 1", bot=False)
        self.player2 = Player(name="Player 2", bot=False)
        self.game_field1 = GameField(self.player1)
        self.game_field2 = GameField(self.player2)

    def test_left_to_place_ships(self):
        # NO IDEA
        pass

    def test_attack_execution(self):
        # set_testing_ship(self.game_field1, 0, 0, 3, "destroyer", "down")
        # set_testing_ship(self.game_field2, 9, 9, 3, "destroyer", "up")
        # self.game.set_last_turn_player(self.player1.get_player_name())

        # with patch("builtins.input", return_value="J1"):
        #    attack_execution(self.game_field1, self.game_field2)

        # self.assertEqual(self.game.get_last_turn_player(), self.player2)
        # self.assertEqual(len(self.game_field2.get_hitfield()), 10)
        # self.assertEqual(self.player1.get_botcache(), [])
        pass


if __name__ == "__main__":
    unittest.main()
