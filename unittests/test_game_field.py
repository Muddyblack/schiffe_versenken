# pylint: disable=C
import unittest
import sys
import os
import re
import io
from string import ascii_uppercase
from unittest.mock import patch
import random

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

from classes.game_field import GameField
from classes.player import Player


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

            text = self.game_field._GameField__get_field_text(field)

            self.assertEqual(
                ansi_escape.sub("", text).replace(" ", "").replace("\x08", ""),
                expected_text,
            )

    def test_get_matrix_size(self):
        size = 2
        self.game_field.set_matrix_size(size)
        self.assertEqual(self.game_field.get_matrix_size(), size)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show_fields(self, mock_stdout):
        matrix_sizes = [
            3,
            5,
            10,
        ]

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
            # RESET
            mock_stdout.seek(0)
            mock_stdout.truncate()

            self.game_field.show_hitfield()
            self.assertEqual(
                ansi_escape.sub("", mock_stdout.getvalue())
                .replace(" ", "")
                .replace("\x08", ""),
                expected_text,
            )
            # RESET
            mock_stdout.seek(0)
            mock_stdout.truncate()

    def test_set_ship_borders(self):
        # Set the input to (0, 0), which is equivalent to "A1"
        matrix_max = 9  # 0...9 -> len == 10
        directions = ["right", "left", "up", "down"]

        shiptype = "destroyer"
        shiplen = 3

        for row in range(matrix_max):
            for column in range(matrix_max):
                with patch.object(
                    GameField,
                    "_GameField__get_row_and_column_input",
                    return_value=(row, column),
                ):
                    print(row, column)
                    for direction in directions:
                        with patch(
                            "keyboard.is_pressed",
                            side_effect=lambda key: key == direction,
                        ):
                            result = self.game_field.set_ship(
                                ship_len=shiplen, ship_type=shiptype, is_bot=False
                            )
                            the_boolean = True

                            if (
                                ((row < shiplen - 1) and direction == "up")
                                or (
                                    (row > matrix_max - shiplen + 1)
                                    and direction == "down"
                                )
                                or ((column < shiplen - 1) and direction == "left")
                                or (
                                    (column > matrix_max - shiplen + 1)
                                    and direction == "right"
                                )
                            ):
                                the_boolean = False

                            self.assertEqual(result, the_boolean)
                            # reset field for next check
                            self.game_field.set_boatfield(self.game_field.init_field())

    def test_user_get_position_input(self):
        valid_inputs = ["A1", "1A", "B3", "4C"]
        valid_results = [(0, 0), (0, 0), (2, 1), (3, 2)]

        for index, input_txt in enumerate(valid_inputs):
            with patch("builtins.input", return_value=input_txt):
                result = self.game_field._GameField__get_row_and_column_input(
                    "Enter your position:", False
                )
                self.assertEqual(result, valid_results[index])

        invalid_inputs = ["D0", "D20", "Eß", "11", "132"]
        invalid_result = [
            "Outside of the Field!",
            "Outside of the Field!",
            "Not a valid Input! Please try again!",
            "Not a valid Input! Please try again!",
            "Not a valid Input! Please try again!",
        ]

        for index, input_txt in enumerate(invalid_inputs):
            with patch("builtins.input", side_effect=input_txt):
                self.game_field._GameField__get_row_and_column_input(
                    "Enter your position:", False
                )

                with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
                    self.assertEqual(fake_stdout.getvalue(), invalid_result[index])

                    # RESET
                    fake_stdout.seek(0)
                    fake_stdout.truncate()

    @patch("random.randint", side_effect=[2, 3])
    def test_bot_input(self, mock_randint):
        random.seed(1)  # set the seed for reproducibility

        # Test bot input
        row, col = self.game_field._GameField__get_row_and_column_input(
            "Enter coordinates: ", True
        )
        self.assertEqual(row, 2)
        self.assertEqual(col, 3)

    def test_ship_surrounding_check(self):
        shiplen = 3
        set_testing_ship(self.game_field, 0, 0, shiplen, "destroyer", "down")
        orientations = ["vertical", "horizontal"]

        for orientation in orientations:
            self.assertEqual(
                self.game_field._GameField__check_ship_surrounding(
                    orientation, shiplen, 0, 1
                ),
                False,
            )

        for orientation in orientations:
            self.assertEqual(
                self.game_field._GameField__check_ship_surrounding(
                    orientation, shiplen, 0, 3
                ),
                True,
            )

        for orientation in orientations:
            self.assertEqual(
                self.game_field._GameField__check_ship_surrounding(
                    orientation, shiplen, 4, 1
                ),
                True,
            )


class TestAttackEnemy(unittest.TestCase):
    def setUp(self):
        # Set up some test data
        self.player1 = Player(name="Chrissi", bot=False)
        self.player2 = Player(name="Linus", bot=False)
        self.game_field1 = GameField(self.player1)
        self.game_field2 = GameField(self.player2)

        set_testing_ship(self.game_field1, 0, 0, 3, "destroyer", "right")
        set_testing_ship(self.game_field2, 3, 2, 3, "destroyer", "down")

    def test_attack_enemy_self(self):
        # Test that the attack raises a ValueError when the player attacks themselves
        with self.assertRaises(ValueError):
            self.game_field1.attack_enemy(self.game_field1)

    def test_attack_enemy_hit(self):
        # Test that the attack hits the enemy's ship
        with patch.object(
            GameField,
            "_GameField__get_row_and_column_input",
            return_value=(3, 2),
        ):
            self.game_field1.attack_enemy(self.game_field2)

        self.assertEqual(self.game_field2.get_boatfield()[3][2], "X")
        self.assertEqual(self.game_field1.get_hitfield()[3][2], 1)

    def test_attack_enemy_miss(self):
        # Test that the attack misses the enemy's ship
        with patch.object(
            GameField,
            "_GameField__get_row_and_column_input",
            return_value=(0, 0),
        ):
            self.game_field1.attack_enemy(self.game_field2)
        self.assertEqual(self.game_field2.get_boatfield()[0][0], 0)
        self.assertEqual(self.game_field1.get_hitfield()[0][0], "o")

    def test_attack_enemy_win(self):
        # Test that the attack results in a win
        with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
            with patch.object(
                GameField,
                "_GameField__get_row_and_column_input",
                return_value=(3, 2),
            ):
                self.game_field1.attack_enemy(self.game_field2)
            with patch.object(
                GameField,
                "_GameField__get_row_and_column_input",
                return_value=(4, 2),
            ):
                self.game_field1.attack_enemy(self.game_field2)
            with patch.object(
                GameField,
                "_GameField__get_row_and_column_input",
                return_value=(5, 2),
            ):
                self.game_field1.attack_enemy(self.game_field2)
        self.assertIn(
            f"Congrats {self.player1.get_player_name()}, YOU WON!",
            ansi_escape.sub("", fake_stdout.getvalue()),
        )
        # RESET
        fake_stdout.seek(0)
        fake_stdout.truncate()

    def test_attack_enemy_bot(self):
        # Test that the attack works when the player is a bot
        self.player1.set_bot(True)
        with patch.object(
            GameField,
            "_GameField__get_row_and_column_input",
            return_value=(3, 2),
        ):
            self.game_field1.attack_enemy(self.game_field2)
        self.assertEqual(self.game_field2.get_boatfield()[3][2], "X")


if __name__ == "__main__":
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/test_game_field.log", "w"
    ) as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner)

    unittest.main()
