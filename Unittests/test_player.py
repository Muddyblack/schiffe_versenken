# pylint: disable=C)
import unittest
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

from Classes.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_get_bot(self):
        self.assertEqual(self.player.get_bot(), False)

    def test_get_player_name(self):
        self.assertEqual(self.player.get_player_name(), "Player")

    def test_get_ships(self):
        self.assertEqual(
            self.player.get_ships(),
            {"battleship": [], "cruiser": [], "destroyer": [], "uboat": []},
        )

    def test_get_ship_amount(self):
        self.assertEqual(self.player.get_ship_amount(), 0)

    def test_set_bot(self):
        self.player.set_bot(True)
        self.assertEqual(self.player.get_bot(), True)

    def test_set_player_name(self):
        self.player.set_player_name("John")
        self.assertEqual(self.player.get_player_name(), "John")

    def test_set_ships(self):
        ships = {
            "battleship": [(0, 0)],
            "cruiser": [(1, 1)],
            "destroyer": [(2, 2)],
            "uboat": [(3, 3)],
        }
        self.player.set_ships(ships)
        self.assertEqual(self.player.get_ships(), ships)

    def test_ships_after_attack(self):
        # Set up ships for testing
        ships = {
            "battleship": [(0, 0), (0, 1)],
            "cruiser": [(1, 1)],
            "destroyer": [(2, 2)],
            "uboat": [(3, 3)],
        }
        self.player.set_ships(ships)

        # Test attack on a cell with a ship
        self.player.ships_after_attack((0, 0))
        self.assertEqual(
            self.player.get_ships(),
            {
                "battleship": [(0, 1)],
                "cruiser": [(1, 1)],
                "destroyer": [(2, 2)],
                "uboat": [(3, 3)],
            },
        )

        # Test attack on a cell without a ship
        self.player.ships_after_attack((5, 5))
        self.assertEqual(
            self.player.get_ships(),
            {
                "battleship": [(0, 1)],
                "cruiser": [(1, 1)],
                "destroyer": [(2, 2)],
                "uboat": [(3, 3)],
            },
        )

        # Test attack that destroys a ship
        self.player.ships_after_attack((0, 1))
        self.assertEqual(
            self.player.get_ships(),
            {
                "battleship": [],
                "cruiser": [(1, 1)],
                "destroyer": [(2, 2)],
                "uboat": [(3, 3)],
            },
        )

    def test_add_ship(self):
        self.player.add_ship("battleship", (0, 0))
        self.assertEqual(
            self.player.get_ships(),
            {"battleship": [(0, 0)], "cruiser": [], "destroyer": [], "uboat": []},
        )


if __name__ == "__main__":
    unittest.main()
