# pylint: disable=C)
import unittest
import sys
import os
import re
import io
from string import ascii_uppercase
from unittest.mock import patch

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

from classes.game_field import GameField
from classes.player import Player


class TestGameField(unittest.TestCase):
    def setUp(self):
        # Set up the GameField object for testing
        self.game_field = GameField(Player(name="Player", bot=False))

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

    def test_matrix_size(self):
        test_sizes = [1, 5, 10]
        for size in test_sizes:
            self.game_field.set_matrix_size(size)
            matrix = self.game_field.init_field()
            self.assertEqual(len(matrix), size)
            for x in range(len(matrix)):
                self.assertEqual(len(matrix[x]), size)

    def test_get_field_text(self):
        matrix_sizes = [3, 5, 10]

        for matrix_size in matrix_sizes:
            self.game_field.set_matrix_size(matrix_size)
            field = []
            expected_text = f"{ascii_uppercase[0:(matrix_size)]}\n"
            for x in range(matrix_size):
                expected_text += str(x + 1) + "~" * matrix_size + "\n"
                field.append([0 for i in range(matrix_size)])

            ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
            text = self.game_field._GameField__get_field_text(field)

            self.assertEqual(
                ansi_escape.sub("", text).replace(" ", "").replace("\x08", ""),
                expected_text,
            )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show_fields(self, mock_stdout):
        matrix_sizes = [
            3,
            5,
            10,
        ]  # warum auch immer resetted er die variable expected_text nicht in der Schleife muss and mock stdout liegen

        for matrix_size in matrix_sizes:
            self.game_field.set_matrix_size(matrix_size)
            field = []

            expected_text = f"{ascii_uppercase[0:(matrix_size)]}\n"

            for x in range(matrix_size):
                expected_text += str(x + 1) + "~" * matrix_size + "\n"
                field.append([0 for i in range(matrix_size)])

            expected_text += "\n"

            self.game_field.set_boatfield(field)
            self.game_field.set_hitfield(field)
            ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

            self.game_field.show_boatfield()
            self.assertEqual(
                ansi_escape.sub("", mock_stdout.getvalue())
                .replace(" ", "")
                .replace("\x08", ""),
                expected_text,
            )

    def set_ship(self):
        pass


if __name__ == "__main__":
    unittest.main()
