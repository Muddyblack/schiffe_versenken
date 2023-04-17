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
    This class defines the game field, which holds information about ships positions and shots in the game.
    It has several methods to display the field and modify the field with the addition of ships and shots.
    """

    def __init__(self, owner):
        random.seed(datetime.now().timestamp())

        self.owner = owner
        self.__ships_left = 10
        self.__fsize = 10
        self.__hitfield = [
            [0 * i for j in range(self.__fsize)] for i in range(self.__fsize)
        ]
        self.__boatfield = self.__hitfield
        self.__botcache = []

    # getter
    def get_boatfield(self):
        """Returns the boatfield matrix."""
        return self.__boatfield

    def get_hitfield(self):
        """Returns the hitfield matrix."""
        return self.__hitfield

    def get_ships_left(self):
        """Returns the current living ships"""
        return self.__ships_left

    # setter
    def set_boatfield(self, field):
        """Sets the boatfield matrix."""
        self.__boatfield = field

    def set_hitfield(self, field):
        """Sets the hitfield matrix."""
        self.__hitfield = field

    def set_boatfield_cell(self, row, col, value=0):
        """Sets the value of a cell in the boatfield matrix."""
        self.__boatfield[row][col] = value

    def set_hitfield_cell(self, row, col, value=1):
        """Sets the value of a cell in the hitfield matrix."""
        self.__hitfield[row][col] = value

    def set_ships_left(self, value):
        """Sets the current living ships"""
        self.__ships_left = value

    # Show Field Functions
    def show_field(self, fieldtype):
        """
        Prints Field with Postion Indictaros at the top and left, like A1, B10, etc.
        """

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
        """Prints the boatfield matrix."""
        self.show_field(self.__boatfield)

    def show_hitfield(self):
        """Prints the hitfield matrix."""
        self.show_field(self.__hitfield)

    # Ship placement functions
    def __check_ship_surrounding(self, orientation, shiplength, boat_row, boat_column):
        """
        Checks if the position of a new boat to be placed in the game field is valid:
            - boat is not too close to or crossing another boat,
        It examines the surrounding positions
        Returns:
            bool: True if the position is valid
        """
        if orientation == "vertical":
            for i in range(-1, 1):
                for j in range(shiplength + 2):
                    checkfield = self.__boatfield[boat_row - 1 + j][boat_column + i]
                    if checkfield == 1:
                        print(
                            "Not an allowed position. Your wantedBoat is too close or crossing another one!"
                        )
                        return False
        elif orientation == "horizontal":
            for i in range(-1, 1):
                for j in range(shiplength + 2):
                    checkfield = self.__boatfield[boat_row + i][boat_column - 1 + j]
                    if checkfield == 1:
                        print(
                            "Not an allowed position. Your wanted Boat is too close or crossing another one!"
                        )
                        return False
        return True

    def set_ship(self, shiplength):
        """
        Asks the player for the start location and direction of a ship of the given length and sets it on the game field.
        """

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
                # Boot in Feld plazieren Entweder von oben nach unten, oder von links nach recht
                if orientation == "vertical":
                    for i in range(shiplength):
                        self.__boatfield[boat_row + i][boat_column] = 1
                elif orientation == "horizontal":
                    for i in range(shiplength):
                        self.__boatfield[boat_row][boat_column + i] = 1
                break

    def attack_enemy(self, target):
        """
        Attacks the enemy's boat at the specified position.
        """
        if self == target:
            raise ValueError("You cannot attack yourself!")

        # If the player is a bot, randomly choose a position that has not been used before to attack
        if self.owner.get_bot() is True:
            while True:
                col = random.randint(0, self.__fsize - 1)
                row = random.randint(0, self.__fsize - 1)

                if [col, row] not in self.__botcache:
                    self.__botcache.append([col, row])
                    break

        # Otherwise, prompt the player to choose a position to attack
        else:
            while True:
                pos = input("Enter the atttacking position for your ship (e.g. A1): ")
                try:
                    col = ascii_uppercase.index(pos[0])
                    row = int(pos[1:]) - 1
                except (IndexError, InterruptedError, ValueError):
                    continue
                break

        # Check if the attack hits a ship or not
        # And if it hits a ship, the player gets to attack again
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
