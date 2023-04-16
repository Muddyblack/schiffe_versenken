import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)
#pylint: disable=wrong-import-position
from main import place_all_ships
import unittest
from hypothesis import given
import hypothesis.strategies as st
from Classes.game_field import GameField


#@given(st.one_of(st.text() or st.integers(min_value=1, max_value=4)))
#def test_place_all_ships(current_boat_to_place):
#    boat = current_boat_to_place
#    assert boat == "battleship" or "1" or "cruiser" or "2" or "destroyer" or "3" or "uboat" or "4"

@given(st.builds(GameField))
def test_place_all_ships(player):
    place_all_ships(player)
    assert player.are_all_ships_placed()