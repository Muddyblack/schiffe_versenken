# pylint: disable=C
import unittest
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

from classes.player import Player


class TestPlayer(unittest.TestCase):
    """Class to Test all functionalities of the Class: Player"""

    def setUp(self):
        """Sets standard player for testing"""
        self.player = Player(name="Ullrich", bot=False)

    def test_get_bot(self):
        """checks that player is not indicated as bot"""
        self.assertEqual(self.player.get_bot(), False)

    def test_get_bot_cache(self):
        """Checks that starter cache is empty"""
        self.assertEqual(self.player.get_botcache(), [])

    def test_get_player_name(self):
        """Checks for correct name return"""
        self.assertEqual(self.player.get_player_name(), "Ullrich")

    def test_get_ships(self):
        """checking if standard ships are used"""
        self.assertEqual(
            self.player.get_ships(),
            {"battleship": [], "cruiser": [], "destroyer": [], "submarine": []},
        )

    def test_get_ship_amount(self):
        """checks if correct ship amount gets returned"""
        self.assertEqual(self.player.get_ship_amount(), 0)

    def test_set_bot(self):
        """Check if setting palyer as bot works"""
        self.player.set_bot(True)
        self.assertEqual(self.player.get_bot(), True)

    def test_set_player_name(self):
        """checks if correct naming works"""
        self.player.set_player_name("John")
        self.assertEqual(self.player.get_player_name(), "John")

    def test_set_ships(self):
        """checks if it sets ships properly"""
        ships = {
            "battleship": [[(0, 0)]],
            "cruiser": [[(1, 1)]],
            "destroyer": [[(2, 2)]],
            "submarine": [[(3, 3)]],
        }
        self.player.set_ships(ships)
        self.assertEqual(self.player.get_ships(), ships)

    def test_ships_after_attack(self):
        """Checks if ships get removed correctly after an attack"""
        ships = {
            "battleship": [[(0, 0), (0, 1)], [(10, 0), (10, 1)]],
            "cruiser": [[(1, 1)]],
            "destroyer": [[(2, 2)]],
            "submarine": [[(3, 3)]],
        }
        self.player.set_ships(ships)

        # Testing attack on a cell with a ship
        self.player.ships_after_attack((0, 0))
        self.assertEqual(
            self.player.get_ships(),
            {
                "battleship": [[(0, 1)], [(10, 0), (10, 1)]],
                "cruiser": [[(1, 1)]],
                "destroyer": [[(2, 2)]],
                "submarine": [[(3, 3)]],
            },
        )

        self.player.ships_after_attack((5, 5))
        self.assertEqual(
            self.player.get_ships(),
            {
                "battleship": [[(0, 1)], [(10, 0), (10, 1)]],
                "cruiser": [[(1, 1)]],
                "destroyer": [[(2, 2)]],
                "submarine": [[(3, 3)]],
            },
        )
        # Destroying first battleship
        self.player.ships_after_attack((0, 1))
        self.assertEqual(
            self.player.get_ships(),
            {
                "battleship": [[(10, 0), (10, 1)]],
                "cruiser": [[(1, 1)]],
                "destroyer": [[(2, 2)]],
                "submarine": [[(3, 3)]],
            },
        )

        self.player.ships_after_attack((10, 1))
        self.assertEqual(
            self.player.get_ships(),
            {
                "battleship": [[(10, 0)]],
                "cruiser": [[(1, 1)]],
                "destroyer": [[(2, 2)]],
                "submarine": [[(3, 3)]],
            },
        )
        # destroying second battleship
        self.player.ships_after_attack((10, 0))
        self.assertEqual(
            self.player.get_ships(),
            {
                "battleship": [],
                "cruiser": [[(1, 1)]],
                "destroyer": [[(2, 2)]],
                "submarine": [[(3, 3)]],
            },
        )

        self.assertEqual(self.player.get_ship_amount(), 3)

    def test_add_ship(self):
        """Checks if it is adding ships correctly"""
        self.player.add_ship("battleship", [(0, 0)])
        self.assertEqual(
            self.player.get_ships(),
            {"battleship": [[(0, 0)]], "cruiser": [], "destroyer": [], "submarine": []},
        )


if __name__ == "__main__":
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/logging/test_player.log",
        "w",
        encoding="utf-8",
    ) as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner)

    unittest.main()
