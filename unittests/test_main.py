# pylint: disable=C
import sys
import os
import io
import re
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

from classes.player import Player
from classes.game_field import GameField
from classes.game import Game

from main import left_to_place_ships, place_all_ships, attack_execution

# Allows to remove ansi_escpaes from game output
ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

from test_game_field import set_testing_ship


class TestGameFuncs(unittest.TestCase):
    """Class to test a bit the main.py file"""

    def setUp(self):
        """Setting up existing ships and their types and Players with their Field for this Testing"""
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
        """Testing the text creation for remaining ships that need to be placed"""
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
        """Also testing the preview-text but this time with some existing ships"""
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
        """Testing walkthrough of attacking each other"""

        set_testing_ship(self.game_field1, (0, 0), 3, "submarine", "down")
        set_testing_ship(self.game_field2, (9, 9), 3, "submarine", "up")

        self.game.set_last_turn_player(self.player1.get_player_name())

        with patch("builtins.input", return_value="J10"):
            attack_execution(attacker=self.game_field1, target=self.game_field2)
            self.assertEqual(
                self.game.get_last_turn_player(), self.player1.get_player_name()
            )
            self.assertNotEqual(self.game_field1.get_hitfield()[1][1], "X")

        with patch("builtins.input", return_value="J9"):
            attack_execution(attacker=self.game_field1, target=self.game_field2)
            self.assertEqual(
                self.game.get_last_turn_player(), self.player1.get_player_name()
            )
            self.assertEqual(self.game_field1.get_hitfield()[9][9], "X")
        # check water hit
        with patch("builtins.input", return_value="F1"):
            attack_execution(attacker=self.game_field1, target=self.game_field2)
            self.assertEqual(
                self.game.get_last_turn_player(), self.player1.get_player_name()
            )
            self.assertEqual(self.game_field1.get_hitfield()[0][5], "o")

        # check winning
        with patch("builtins.input", return_value="J8"):
            try:
                attack_execution(attacker=self.game_field1, target=self.game_field2)
                self.assertEqual(
                    self.game.get_last_turn_player(), self.player2.get_player_name()
                )
                self.assertEqual(self.game_field1.get_hitfield()[1][1], 1)
            except SystemExit:
                pass

    @patch("builtins.input", side_effect=["1", "8"])
    @patch("simpleaudio.WaveObject.from_wave_file", return_value=MagicMock())
    @patch("library.console_helper.clear_console", return_value=None)
    def test_player_places_all_ships(
        self, mock_clear_console, mock_play_sound, mock_input
    ):
        """Trying to place all ships that are indicated below"""
        obj = MagicMock()
        obj.owner.get_ship_preferences.return_value = {
            "battleship": {"length": 5, "max": 1},
            "destroyer": {"length": 4, "max": 2},
        }
        obj.owner.get_ships.return_value = {"battleship": [], "destroyer": []}
        obj.show_boatfield.return_value = None
        obj.set_ship.side_effect = [True, True, True]

        try:
            place_all_ships(obj)

            self.assertEqual(obj.set_ship.call_count, 4)
            self.assertEqual(mock_clear_console.call_count, 3)
            self.assertEqual(mock_play_sound.call_count, 0)
            obj.show_boatfield.assert_called_once()
            self.assertEqual(mock_input.call_count, 1)
        except StopIteration:
            pass

        try:
            with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
                place_all_ships(obj)

                self.assertEqual(
                    ansi_escape.sub("", fake_stdout.getvalue()).replace(" ", ""),
                    "UnknownBoat-Type.",
                )
                # RESET
                fake_stdout.seek(0)

                self.assertEqual(obj.set_ship.call_count, 4)
                self.assertEqual(mock_clear_console.call_count, 3)
                self.assertEqual(mock_play_sound.call_count, 0)
                obj.show_boatfield.assert_called_once()
                self.assertEqual(mock_input.call_count, 1)
        except StopIteration:
            pass


if __name__ == "__main__":
    unittest.main()
