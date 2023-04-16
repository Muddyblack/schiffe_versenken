"""
The GameField class represents the game board and handles all game logic.

This module requires the following external libraries to be installed:
- keyboard

"""
import sys
import os
from string import ascii_uppercase
from datetime import datetime
import random

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)
# pylint: disable=wrong-import-position
from Library.keyboard_helper import get_arrow_key

# anicode
BLUE = "\033[0;34m"
RED = "\033[0;31m"
RESET = "\033[0m"


class GameField:
    """
    This class defines the game field, which holds information about the player, positions of ships and shots in the game.
    It has several methods to display the field and modify the field with the addition of ships and shots.
    """

    def __init__(self, bot=False, name="Player"):
        random.seed(datetime.now().timestamp())

        self.__fsize = 10
        self.__current_turn = False
        self.__hitfield = [
            [0 * i for j in range(self.__fsize)] for i in range(self.__fsize)
        ]
        self.__boatfield = self.__hitfield

        self.__bot = bot
        self.__botcache = []
        if bot is True:
            self.__player_name = "bot"
        else:
            self.__player_name = name

    def show_field(self, fieldtype):
        # Print Field with Postion Indictaros at the top and left, like A1, B10, etc to the Command-Line
        print(" " * (len(str(self.__fsize)) + 2), end="")
        for elem in range(self.__fsize):
            print(f"{ascii_uppercase[elem]}", end=" ")
        print("\n")

        for num, line in enumerate(fieldtype, 1):
            print(f"{num}", end="   ")

            if len(str(num)) > 1:
                print("\b" * (len(str(num)) - 1), end="")
            for row in line:
                if row == 1:
                    color = BLUE
                elif row == "X":
                    color = RED
                else:
                    color = RESET
                print(color + str(row), end=" ")
            print("")
        print("\n")

    def show_boatfield(self):
        self.show_field(self.__boatfield)

    def show_hitfield(self):
        self.show_field(self.__hitfield)

    # getter
    def get_bot(self):
        return self.__bot

    def get_boatfield(self):
        return self.__boatfield

    def get_hitfield(self):
        return self.__hitfield

    def get_player_name(self):
        return self.__player_name

    def get_current_turn(self):
        return self.__current_turn

    # setter
    def set_boatfield(self, field):
        self.__boatfield = field

    def set_hitfield(self, field):
        self.__hitfield = field

    def set_boatfield_cell(self, row, col, value=0):
        self.__boatfield[row][col] = value

    def set_hitfield_cell(self, row, col, value=1):
        self.__hitfield[row][col] = value

    def set_current_turn(self, value):
        self.__current_turn = value

    def __check_ship_surrounding(self, orientation, shiplength, boat_row, boat_column):
        for i in range(-1, shiplength + 1):
            if orientation == "horizontal":
                row = boat_row + i
                col = boat_column - 1 + i
            else:
                row = boat_row - 1 + i
                col = boat_column + i
            if (
                row < 0
                or row >= len(self.__boatfield)
                or col < 0
                or col >= len(self.__boatfield[row])
            ):
                continue
            if self.__boatfield[row][col] == 1:
                print(
                    "Not an allowed position. Your wanted Boat is too close or crossing another one!"
                )
                return False
        return True

    def set_ship(self, shiplength):
        # asks startlocation and direction via arrows
        # check not over field size and not already set

        while True:
            # ask start location
            start_pos = input(
                f"Enter the start position for your ship {shiplength} long ship (e.g. A1): "
            )
            try:
                start_col = ascii_uppercase.index(start_pos[0])
                start_row = int(start_pos[1:]) - 1
            except (IndexError, InterruptedError, ValueError):
                continue

            print("Enter the direction for your ship. Use your arrow Keys!")
            direction = get_arrow_key()
            # Bei up und down ist start und end_col gleich
            # Bei right and left ist start und end_row gleich
            if direction == "up":
                boat_column = start_col
                boat_row = start_row - (shiplength - 1)
                orientation = "vertical"
            elif direction == "down":
                boat_column = start_col
                boat_row = start_row
                orientation = "vertical"
            elif direction == "left":
                boat_column = start_col - (shiplength - 1)
                boat_row = start_row
                orientation = "horizontal"
            elif direction == "right":
                boat_column = start_col
                boat_row = start_row
                orientation = "horizontal"
            else:
                print("Invalid direction!")
                continue
            print(direction)

            # check if ship fits on the board
            if (
                boat_column >= self.__fsize
                or boat_column < 0
                or boat_row >= self.__fsize
                or boat_row < 0
            ):
                print(
                    "Ship does not fit on the board. Please choose a different start position or direction."
                )
                continue

            valid = self.__check_ship_surrounding(
                orientation, shiplength, boat_row, boat_column
            )

            if valid:
                # Boot in Feld plazieren Entweder von oben nach unten, oder von links nach rechts
                if orientation == "vertical":
                    self.__boatfield[boat_row : boat_row + shiplength, boat_column] = 1
                else:
                    self.__boatfield[
                        boat_row, boat_column : boat_column + shiplength
                    ] = 1
                break

    def attack_enemy(self, target):
        placed = False

        if self.__bot is True:
            while True:
                col = random.randint(0, self.__fsize - 1)
                row = random.randint(0, self.__fsize - 1)

                if [col, row] not in self.__botcache:
                    self.__botcache.append([col, row])
                    break

        else:
            while not placed:
                # ask start location
                pos = input("Enter the atttacking position for your ship (e.g. A1): ")
                try:
                    col = ascii_uppercase.index(pos[0])
                    row = int(pos[1:]) - 1
                except (IndexError, InterruptedError, ValueError):
                    continue
                placed = True

        if target.get_boatfield()[row][col] == 1:
            print("Sir, we hitted an enemy target!")
            self.__hitfield[row][col] = 1
            target.set_boatfield_cell(row, col, "X")
            self.show_hitfield()
            print("You can attack a second time")
            self.attack_enemy(target)
        elif target.get_boatfield()[row][col] == "X":
            print("We already hit this Part")
        else:
            print("Sir we've hit the bull's eye!")


if __name__ == "__main__":
    x1 = GameField(name="Petra", bot=False)
    x1.set_ship(5)
    x1.set_ship(5)
    x1.show_boatfield()
