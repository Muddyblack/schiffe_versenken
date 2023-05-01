# pylint: disable=C)
import unittest
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)
from unittest.mock import patch
from classes.game import Game
from classes.game import Player


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.player1 = Player("Lena")
        self.player2 = Player("Lara")
        self.game.__players = [self.player1, self.player2]

    def test_get_players(self):
        player1 = Player("Lena")
        player2 = Player("Lara")
        self.game.set_players(player1)
        self.assertEqual(self.game.get_players(), player1)
        self.game.set_players(player2)
        self.assertEqual(self.game.get_players(), player2)


    def test_get_current_level(self):
        self.game.set_current_level(1)
        self.assertEqual(self.game.get_current_level(), 1)  # level 0 schiffe platziert level 1 attacken

    def test_get_last_turn_player(self):
        self.game.set_last_turn_player("Lena")
        self.assertEqual(self.game.get_last_turn_player(), "Lena")

    def test_set_players(self):
        players = {"Lena", "Lara"}
        self.game.set_players(players)
        self.assertEqual(self.game.get_players(), {"Lena", "Lara"})

    def test_set_current_level(self):
        level = 1
        self.game.set_current_level(level)
        self.assertEqual(self.game.get_current_level(), level)  # oder anstatt level 1

    def test_set_last_turn_player(self):
        player1 = Player("Lena")
        player2 = Player("Lara")
        self.game.set_last_turn_player(player1)
        self.assertEqual(self.game.get_last_turn_player(), player1)
        self.game.set_last_turn_player(player2)
        self.assertEqual(self.game.get_last_turn_player(), player2)

    def test_ask_name(self):
        user_input = ['Luisa']
        with patch('builtins.input', side_effect=user_input):
            game = Game()
            #_Game ist eine interne Klasse
            result = game._Game__ask_name("What's your name?")
            self.assertEqual(result, "Luisa")

    def test__yes_no_question(self):
        game = Game()
        #testing multiple inputs
        with patch('builtins.input', side_effect=['y', 'yes', '' , 'n', 'no']):
            self.assertTrue(game._Game__yes_no_question("Do you want to continue?"))
            self.assertTrue(game._Game__yes_no_question("Do you want to continue?"))
            self.assertTrue(game._Game__yes_no_question("Do you want to continue?"))
            self.assertFalse(game._Game__yes_no_question("Do you want to continue?"))
            self.assertFalse(game._Game__yes_no_question("Do you want to continue?"))
    
    """
    def test__display_save_games(self):
        game = Game()
        with patch("builtins.print" ) as mock_print:
            game._Game__display_save_games(["save_game1", "save_game2", "save_game3"], 1)
            mock_print.assert_called_with("save_game1 >save_game2  save_game3")       
    """
    
    def test_start_up(self):
        game = Game()
        exist_save_game=[]
        result=game._Game__start_up(exist_save_game)
        self.assertEqual(result, self.__create_new_game())
    
        
if __name__ == "__main__":
    unittest.main()
