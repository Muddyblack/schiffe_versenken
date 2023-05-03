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
            "battleship": {"length": 5, "max": 1},
            "destroyer": {"length": 4, "max": 2},
            "cruiser": {"length": 3, "max": 3},
            "submarine": {"length": 2, "max": 4},
        }

        self.ships = {
            "battleship": [],
            "destroyer": [],
            "cruiser": [],
            "submarine": [],
        }

        self.game = Game()
        self.player1 = Player(name="Player 1", bot=False)
        self.player2 = Player(name="Player 2", bot=False)
        self.game_field1 = GameField(self.player1)
        self.game_field2 = GameField(self.player2)

    def test_left_to_place_ships(self):
        expected_print_text = (
            "You have\n"
            "1: battleship 1 (5-Long)\n"
            "2: destroyer 2 (4-Long)\n"
            "3: cruiser 3 (3-Long)\n"
            "4: submarine 4 (2-Long)"
        )
        expected_ships_left = 10
        expected_placed_ships = []

        result = left_to_place_ships(self.ship_types, self.ships)

        self.assertEqual(
            ansi_escape.sub("", result[0]).replace(" ", ""),
            (expected_print_text + "\n\nWhich Ship would you like to place?").replace(
                " ", ""
            ),
        )
        self.assertEqual(result[1], expected_ships_left)
        self.assertEqual(result[2], expected_placed_ships)

    def test_left_to_place_ships_with_ships_placed(self):
        self.ships = {
            "battleship": [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]],
            "destroyer": [[(0, 6), (0, 7), (0, 8), (0, 9)]],
            "cruiser": [[(2, 0), (3, 0), (4, 0)]],
            "submarine": [[(9, 9), (8, 9)]],
        }

        expected_print_text = (
            "You have\n"
            "1: battleship 0 (5-Long)\n"
            "2: destroyer 1 (4-Long)\n"
            "3: cruiser 2 (3-Long)\n"
            "4: submarine 3 (2-Long)"
        )
        expected_ships_left = 6
        expected_placed_ships = [1]

        result = left_to_place_ships(self.ship_types, self.ships)

        self.assertEqual(
            ansi_escape.sub("", result[0]).replace(" ", ""),
            (expected_print_text + "\n\nWhich Ship would you like to place?").replace(
                " ", ""
            ),
        )
        self.assertEqual(result[1], expected_ships_left)
        self.assertEqual(result[2], expected_placed_ships)

    def test_attack_execution(self):
        set_testing_ship(self.game_field1, 0, 0, 3, "submarine", "down")
        set_testing_ship(self.game_field2, 9, 9, 3, "submarine", "up")
        self.game.set_last_turn_player(self.player1.get_player_name())

        with patch("builtins.input", side_effect=["J10", "J9", "F1"]):
            attack_execution(self.game_field1, self.game_field2)

        self.assertEqual(
            self.game.get_last_turn_player(), self.player2.get_player_name()
        )
        self.assertEqual(self.game_field1.get_hitfield()[0, 9], 1)


if __name__ == "__main__":
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/test_main.log",
        "w",
        encoding="utf-8",
    ) as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner)
    unittest.main()
