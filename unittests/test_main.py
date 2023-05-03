# pylint: disable=C
import sys
import os
import unittest
from unittest import mock
import io
import sys
import os
import builtins
from unittest.mock import patch


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)


from game_funcs import left_to_place_ships, place_all_ships, attack_execution


class TestGameFuncs(unittest.TestCase):
    @patch("builtins.input", return_value="1")
    def test_left_to_place_ships(self, mock_input):
        ship_types = {
            "Carrier": {"max": "1", "length": "5"},
            "Battleship": {"max": "1", "length": "4"},
        }
        ships = {"Carrier": [(1, 1)], "Battleship": []}

        expected_text = "You have\n1: Carrier 0 (5-Long)\n2: Battleship 1 (4-Long)"
        expected_ships_left = 1
        expected_placed_ships = [1]

        result = left_to_place_ships(ship_types, ships)

        self.assertEqual(result[0], expected_text)
        self.assertEqual(result[1], expected_ships_left)
        self.assertEqual(result[2], expected_placed_ships)

    @patch("builtins.input", return_value="1")
    def test_place_all_ships(self, mock_input):
        # TODO: write test for place_all_ships function
        pass

    def test_attack_execution(self):
        # TODO: write test for attack_execution function
        pass


if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()
