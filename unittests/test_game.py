# pylint: disable=C
import unittest
import sys
import os
import re
import shutil
import io
import pickle
import keyboard
from unittest.mock import patch, call

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
        self.player1 = Player(name="Player1", bot=False)
        self.player2 = Player(name="Player2", bot=False)
        self.game_field1 = GameField(self.player1)
        self.game_field2 = GameField(self.player2)

        # Initialize the game
        self.game = Game()
        self.game.set_players([self.player1, self.player2])
        self.game.set_current_level(1)
        self.game.set_last_turn_player(self.player1.get_player_name())
        self.game._Game__save_name = "unittests_save"

        self.exist_save_games = ["save1", "save2", "save3"]

    def tearDown(self):
        save_dir = f"{game_paths.SAVE_GAMES_PATH}/{self.game._Game__save_name}"
        if os.path.exists(save_dir):
            shutil.rmtree(save_dir)

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
        self.assertEqual(
            self.game.get_last_turn_player(), self.player1.get_player_name()
        )

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

    def test_save_game(self):
        # Save the game
        self.game.save_game()

        # Assert that the player list and game info was saved correctly
        save_dir = f"{game_paths.SAVE_GAMES_PATH}/{self.game._Game__save_name}"
        with open(f"{save_dir}/players.pkl", "rb") as file:
            player_list = pickle.load(file)
        with open(f"{save_dir}/game_info.pkl", "rb") as file:
            game_info = pickle.load(file)

        self.assertEqual(game_info["last_turn_player"], self.player1.get_player_name())
        self.assertEqual(game_info["level"], 1)
        self.assertIsInstance(player_list, list)
        self.assertTrue(all(isinstance(player, GameField) for player in player_list))

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
        self.game.save_game()
        self.game.load_game()

        self.assertEqual(
            self.game.get_last_turn_player(), self.player1.get_player_name()
        )
        self.assertEqual(self.game.get_current_level(), 1)
        self.assertIsInstance(self.game.get_players(), list)
        self.assertTrue(
            all(isinstance(player, GameField) for player in self.game.get_players())
        )

    def test_create_new_game(self):
        with patch(
            "builtins.input",
            side_effect=[
                self.game._Game__save_name,
                "n",
                self.player1.get_player_name(),
                "n",
                self.player2.get_player_name(),
            ],
        ):
            self.game._Game__create__new_game([], player_num=2)

        self.assertEqual(len(self.game.get_players()), 2)
        self.assertTrue(
            all(isinstance(p.owner, Player) for p in self.game.get_players())
        )
        self.assertEqual(self.game.get_current_level(), 0)
        self.assertIsNotNone(self.game.get_last_turn_player())
        self.assertIsNotNone(self.game._Game__save_name)

    def test_start_screen(self):
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

    @patch("builtins.print")
    @patch.object(keyboard, "is_pressed")
    @patch.object(console_helper, "refresh_console_lines")
    def test_select_savegame(
        self,
        mock_refresh_console_lines,
        mock_is_pressed,
        mock_print,
    ):
        exist_save_games = [
            f"{game_paths.SAVE_GAMES_PATH}/game1",
            f"{game_paths.SAVE_GAMES_PATH}/game2",
            f"{game_paths.SAVE_GAMES_PATH}/game3",
        ]

        mock_is_pressed.side_effect = [
            # Press down once
            False,  # up not pressed
            True,  # down pressed
            False,  # up not pressed
            # Press up once
            True,  # up pressed
            False,  # down not pressed
            # Select game
            False,  # space pressed
        ]
        try:
            self.game._Game__select_savegame(exist_save_games)

            # Check that console_helper.refresh_console_lines was called correctly
            expected_refresh_calls = [
                call(len(exist_save_games)),
                call(len(exist_save_games)),
                call(len(exist_save_games)),
            ]
            self.assertEqual(
                mock_refresh_console_lines.call_args_list, expected_refresh_calls
            )

            # Check that the correct output was printed
            expected_output = [
                "Use up and down arrows to navigate\nUse Spacebar to select the game",
                "> game1",
                "  game2",
                "  game3",
                "  game1",
                "> game2",
                "  game3",
                "> game1",
                "  game2",
                "  game3",
            ]
            actual_output = [
                ansi_escape.sub("", call_args[0][0])
                for call_args in mock_print.call_args_list
            ]
            self.assertEqual(actual_output, expected_output)
        except StopIteration:
            pass

        # Check that the correct save game was selected
        self.assertEqual(self.game._Game__save_name, "unittests_save")


if __name__ == "__main__":
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/test_game.log",
        "w",
        encoding="utf-8",
    ) as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner)
    unittest.main()
