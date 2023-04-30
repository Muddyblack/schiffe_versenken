# pylint: disable=C)
import unittest
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

from Classes.game_field import GameField
from Classes.player import Player


class TestGameField(unittest.TestCase):
    def setUp(self):
        # Set up the GameField object for testing
        self.game_field = GameField(Player())

    def test_get_boatfield(self):
        # Test the get_boatfield() method
        boatfield = self.game_field.get_boatfield()
        self.assertIsInstance(boatfield, list)
        self.assertEqual(len(boatfield), 10)
        self.assertEqual(len(boatfield[0]), 10)

    def test_get_hitfield(self):
        # Test the get_hitfield() method
        hitfield = self.game_field.get_hitfield()
        self.assertIsInstance(hitfield, list)
        self.assertEqual(len(hitfield), 10)
        self.assertEqual(len(hitfield[0]), 10)

    def test_set_boatfield(self):
        # Test the set_boatfield() method
        boatfield = [[0 for _ in range(10)] for _ in range(10)]
        self.game_field.set_boatfield(boatfield)
        self.assertEqual(self.game_field.get_boatfield(), boatfield)

    def test_set_hitfield(self):
        # Test the set_hitfield() method
        hitfield = [[0 for _ in range(10)] for _ in range(10)]
        self.game_field.set_hitfield(hitfield)
        self.assertEqual(self.game_field.get_hitfield(), hitfield)

    def test_set_boatfield_cell(self):
        # Test the set_boatfield_cell() method
        self.game_field.set_boatfield_cell(0, 0, 1)
        self.assertEqual(self.game_field.get_boatfield()[0][0], 1)

    def test_set_hitfield_cell(self):
        # Test the set_hitfield_cell() method
        self.game_field.set_hitfield_cell(0, 0, 1)
        self.assertEqual(self.game_field.get_hitfield()[0][0], 1)


if __name__ == "__main__":
    unittest.main()
