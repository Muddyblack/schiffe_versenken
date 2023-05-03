# pylint: disable=C
import unittest
import sys
import os
import re
import io
import tempfile
import pickle
from unittest.mock import mock_open, patch, call, MagicMock

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

from classes.game import Game
from classes.player import Player
from classes.game_field import GameField

from library import console_helper

ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


class TestGame(unittest.TestCase):
    def setUp(self):
        # Create two players and game field
        player1 = Player(name="Player1", bot=False)
        player2 = Player(name="Player2", bot=False)
        game_field1 = GameField(player1)
        game_field2 = GameField(player2)

        # Initialize the game
        self.game = Game()
        self.game.set_players([player1, player2])
        self.game.set_current_level(1)
        self.game.set_last_turn_player("Player1")
        game_field1.owner = player1

        self.exist_save_games = ["save1", "save2", "save3"]

    # def test_get_save_path(self):
    #    expected_path = f"{tempfile.gettempdir()}/savegames/test_save"
    #    with tempfile.TemporaryDirectory() as temp_dir:
    #        os.makedirs(expected_path)
    #        self.game.set_save_name("test_save")
    #        self.assertEqual(self.game.get_save_path(), expected_path)

    def test_get_players(self):
        players = self.game.get_players()
        self.assertEqual(len(players), 2)
        self.assertTrue(isinstance(players[0], Player))
        self.assertTrue(isinstance(players[1], Player))

    def test_get_current_level(self):
        self.assertEqual(self.game.get_current_level(), 1)

    def test_get_last_turn_player(self):
        self.assertEqual(self.game.get_last_turn_player(), "Player1")

    def test_set_players(self):
        player3 = Player(name="Player3", bot=False)
        self.game.set_players([player3])
        players = self.game.get_players()
        self.assertEqual(len(players), 1)
        self.assertTrue(isinstance(players[0], Player))
        self.assertEqual(players[0].get_player_name(), "Player3")

    def test_set_current_level(self):
        self.game.set_current_level(2)
        self.assertEqual(self.game.get_current_level(), 2)

    def test_set_last_turn_player(self):
        self.game.set_last_turn_player("Player2")
        self.assertEqual(self.game.get_last_turn_player(), "Player2")

    def test_ask_name(self):
        with unittest.mock.patch("builtins.input", return_value="TestPlayer"):
            self.assertEqual(self.game._Game__ask_name("Enter your name"), "TestPlayer")

        with unittest.mock.patch(
            "builtins.input",
            side_effect=["TestPlayer", "DuplicatePlayer", "TestPlayer2", "TestPlayer!"],
        ):
            self.assertEqual(self.game._Game__ask_name("Enter your name"), "TestPlayer")

    # def test_save_game(self):
    #    # Check that save_game creates a valid save file
    #    with tempfile.TemporaryDirectory() as temp_dir:
    #        self.game.set("test_save")
    #        self.game.set_save_path(f"{temp_dir}/savegames/test_save")

    #        self.game.save_game()

    def test_load_game(self):
        # missing
        pass

    def test_yes_no_question(self):
        yes_input = "y"
        no_input = "n"

        # Test "yes" or "y"
        with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
            with patch("builtins.input", return_value=yes_input):
                result = self.game._Game__yes_no_question("Question")
                self.assertEqual(result, True)

        # Test "no" or "n"
        with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
            with patch("builtins.input", return_value=no_input):
                result = self.game._Game__yes_no_question("Question")
                self.assertEqual(result, False)

    def test_create_new_game(self):
        # NO IDEA
        pass

    def test_start_screen(
        self,
    ):
        # NO IDEA
        pass

    def test_display_save_games(self):
        save_games = ["save1.txt", "save2.txt", "save3.txt"]
        selected_index = 1

        # Redirect stdout to an in-memory buffer for testing
        stdout = io.StringIO()
        sys.stdout = stdout
        self.game._Game__display_save_games(save_games, selected_index)

        output = stdout.getvalue().strip()
        sys.stdout = sys.__stdout__

        expected_output = "save1.txt\n> save2.txt\n  save3.txt".replace(" ", "")
        self.assertEqual(ansi_escape.sub("", output.replace(" ", "")), expected_output)

    def test_select_savegame(self):
        # NO IDEA
        pass


if __name__ == "__main__":
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/test_game.log", "w") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner)
    unittest.main()
