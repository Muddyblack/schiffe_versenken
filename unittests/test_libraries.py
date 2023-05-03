# pylint: disable=C
import os
import sys
import io
import tempfile
import unittest

from unittest.mock import patch

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

from library import console_helper
from library import random_helper
from library import file_helper
from library import keyboard_helper


class TestConsoleHelper(unittest.TestCase):
    """Class for testing consolhelper Module"""

    def test_max_line_length(self):
        """check if it returns longest line"""
        lines = ["abc", "defg", "hijklmno"]
        self.assertEqual(console_helper.max_line_length(lines), 8)

    def test_clear_console(self):
        """Just checking for no raising Exception"""
        console_helper.clear_console()

    def test_refresh_console_lines(self):
        """Just checking for no raising Exception"""
        console_helper.refresh_console_lines(2)

    def test_print_side_by_side(self):
        """Try the side by side function. It is very sensible but does a good job for Battleshipgame"""
        strings = ["one\ntwo\nthree", "four\nfive\nsix", "seven\neight\nnine"]

        expected_output = (
            "one        four        seven    \n"
            "two        five        eight    \n"
            "three        six        nine    \n"
        )

        with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
            console_helper.print_side_by_side(strings, padding=4)
            self.assertEqual(fake_stdout.getvalue(), expected_output)

        strings = ["one\ntwo\nthree", "four\n  five\nsix", " seven\neight\nnine"]
        with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
            console_helper.print_side_by_side(strings, padding=4)
            self.assertNotEqual(fake_stdout.getvalue(), expected_output)


class TestRandomFunctions(unittest.TestCase):
    """Class for testing random_helper Module"""

    def test_randint_exc(self):
        """
        Testing if this function returns a number within the range.
        And nothing from the exception list
        """
        start = 1
        end = 10
        exception = [3, 5, 7]
        for i in range(1000):
            res = random_helper.randint_exc(start, end, *exception)
            self.assertTrue(start <= res <= end)
            self.assertNotIn(res, exception)

        # Should return None if complete range is in exception
        start = 1
        end = 3
        exception = [1, 2, 3]
        self.assertIsNone(random_helper.randint_exc(start, end, *exception))


class TestFileHelperFunctions(unittest.TestCase):
    """Class to test file_helper Module"""

    def setUp(self):
        """create some tempory files for testing"""
        self.test_file = tempfile.NamedTemporaryFile(delete=False)

        # write test data to the file
        with open(self.test_file.name, "w", encoding="utf8") as file:
            file.write("line 1\n")
            file.write("line 2\n")
            file.write("line 3\n")

    def tearDown(self):
        """Deletes created files when testing finished"""
        self.test_file.close()
        os.remove(self.test_file.name)

    def test_read_file(self):
        """testing if read_file gets full file-content"""
        expected_output = ["line 1", "line 2", "line 3"]
        actual_output = file_helper.read_file(self.test_file.name)
        self.assertEqual(actual_output, expected_output)

    def test_file_line_replacer(self):
        """testing if replacing line in file works correctly"""
        change_input = ["new line 2", "new line 3"]
        line = [2, 3]
        file_helper.file_line_replacer(self.test_file.name, change_input, line)

        # check file
        expected_output = ["line 1", "new line 2", "new line 3"]
        actual_output = file_helper.read_file(self.test_file.name)
        self.assertEqual(actual_output, expected_output)


class TestGetArrowKey(unittest.TestCase):
    """Class for testing Arrow key input"""

    def setUp(self):
        self.directions = ["up", "down", "left", "right"]

    def test_get_arrow_keys(self):
        """check if returned key value is correct"""
        # checking for every direction
        for direction in self.directions:
            with patch(
                "keyboard.is_pressed", side_effect=lambda key, dir=direction: key == dir
            ):
                result = keyboard_helper.get_arrow_key()
                self.assertEqual(result, direction)

    def test_clear_input(self):
        """check if it really clears the given input"""
        with patch("sys.stdin", new_callable=io.StringIO) as fake_in:
            fake_in.write("some input\n")
            keyboard_helper.clear_input()
            self.assertEqual(fake_in.read(), "")


if __name__ == "__main__":
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/logging/test_libraries.log",
        "w",
        encoding="utf-8",
    ) as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner)

    unittest.main()
