# pylint: disable=C
import unittest
import sys
import os
import re
import io
import pickle
from unittest.mock import mock_open, patch, call, MagicMock, Mock

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

from classes.game import Game
from classes.player import Player
from classes.game_field import GameField

from library import console_helper
from library import game_paths

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

    def test_get_save_path(self):
        expected_path = f"{game_paths.SAVE_GAMES_PATH}/test_save"
        self.game._Game__save_name = "test_save"
        self.assertEqual(self.game.get_save_path(), expected_path)

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

    @patch("builtins.open", create=True)
    @patch("os.makedirs")
    @patch("gc.get_objects")
    def test_save_game(self, mock_get_objects, mock_makedirs, mock_open):
        player_list = [
            GameField(Player(name="Peter", bot=False)),
            GameField(Player(name="Peter1", bot=False)),
            GameField(Player(name="Peter2", bot=False)),
        ]

        game_info = {
            "last_turn_player": "Peter1",
            "level": 2,
        }
        save_dir = f"{game_paths.PROJECT_PATH}/tests/test_save_game_dir"

        expected_calls = [
            ((f"{save_dir}/players.pkl", "wb"),),
            ((f"{save_dir}/game_info.pkl", "wb"),),
        ]
        expected_values = [
            pickle.dumps(player_list),
            pickle.dumps(game_info),
        ]

        # Mocking return value of gc.get_objects()
        mock_get_objects.return_value = player_list

        self.game.save_game()

        mock_makedirs.assert_called_once_with(save_dir, exist_ok=True)
        mock_get_objects.assert_called_once()
        mock_open.assert_has_calls(expected_calls)
        mock_open().write.assert_has_calls([Mock(data=d) for d in expected_values])

        os.rmdir(save_dir)

    def test_yes_no_question(self):
        yes_input = "y"
        no_input = "n"

        # Test "yes" or "y"
        with patch("builtins.input", return_value=yes_input):
            result = self.game._Game__yes_no_question("Question")
            self.assertEqual(result, True)

        # Test "no" or "n"
        with patch("builtins.input", return_value=no_input):
            result = self.game._Game__yes_no_question("Question")
            self.assertEqual(result, False)

    def test_load_game(self):
        # missing
        pass

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
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/test_game.log",
        "w",
        encoding="utf-8",
    ) as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner)
    unittest.main()
