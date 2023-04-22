"""
The GameField class represents the game board and handles all game logic.

This module requires the following external libraries to be installed:
    - keyboard

"""
from string import ascii_uppercase
from datetime import datetime
import random
from copy import deepcopy

from Library.keyboard_helper import get_arrow_key
from Library import console_helper


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
        self.__boatfield = [
            [0 * i for j in range(self.__fsize)] for i in range(self.__fsize)
        ]
        self.__hitfield = deepcopy(self.__boatfield)
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
    def get_field_text(self, fieldtype):
        """
        Returns string of Field with Postion Indictaros at the top and left, like A1, B10, etc.
        """

        txt = " " * (len(str(self.__fsize)) + 2)
        for elem in range(self.__fsize):
            txt += f"{ascii_uppercase[elem]} "
        txt += "\n"

        for num, line in enumerate(fieldtype, 1):
            txt += f"{num}   "
            if len(str(num)) > 1:
                txt += "\b" * (len(str(num)) - 1)
            for row in line:
                if row == 1:
                    color = console_helper.BLUE
                elif row == "X":
                    color = console_helper.RED
                elif row == "o":
                    color = console_helper.LIGHT_GREEN
                else:
                    color = console_helper.RESET
                txt += color + str(row) + " "
            txt += console_helper.RESET + "\n"
        txt += console_helper.RESET
        return txt

    def show_boatfield(self):
        """Prints the boatfield matrix."""
        print(self.get_field_text(self.__boatfield))

    def show_hitfield(self):
        """Prints the hitfield matrix."""
        print(self.get_field_text(self.__hitfield))

    def show_fields_side_by_side(self):
        """Should print the boatfield and the hitfield matrix side by side."""
        padding = 4
        print(
            console_helper.GREEN
            + "Boatfield"
            + " " * ((len(self.__boatfield) * 2) + padding - 1)
            + "Hitfield"
            + console_helper.RESET
        )
        console_helper.print_side_by_side(
            [
                f"{self.get_field_text(self.__boatfield)}",
                f"{self.get_field_text(self.__hitfield)}",
            ],
            padding=padding,
        )

    # Ship placement functions
    def __get_row_and_column_input(self, message, bot):
        """Gets the Field-Coordiantes the user puts in using the message given to it. input Either in A1 or 1A format
        - returns: row, column
        """

        while bot is False:
            user_input = input(f"{message}").strip()

            try:
                l_row = int(user_input[1:]) - 1
                l_col = int(ascii_uppercase.index(user_input[0].upper()))
            except ValueError:
                try:
                    # If the Array is three long, the Number in front might have two digits
                    if len(user_input) == 3:
                        l_row = int(user_input[:2]) - 1
                        l_col = int(ascii_uppercase.index(user_input[3:].upper()))
                    else:
                        l_row = int(user_input[0]) - 1
                        l_col = int(ascii_uppercase.index(user_input[1:].upper()))
                except (IndexError, InterruptedError, ValueError):
                    print("Not a valid Input! Please try again!")
                    continue
            except (IndexError, InterruptedError):
                print("Not a valid Input! Please try again!")
                continue

            # Checks for validility of the input
            if (
                l_row < 0
                or l_col < 0
                or (self.__fsize - 1) < l_row
                or (self.__fsize - 1) < l_col
            ):
                print("Outside of the Field!")
                continue
            # if everyhting is okay, leave Loop
            break
        if bot:
            l_row = random.randint(0, self.__fsize - 1)
            l_col = random.randint(0, self.__fsize - 1)
        return l_row, l_col

    def __check_ship_surrounding(self, orientation, ship_len, boat_row, boat_column):
        """
        Checks if the position of a new boat to be placed in the game field is valid:
            - boat is not too close to or crossing another boat,
        It examines the surrounding positions
        Returns:
            bool: True if the position is valid
        """
        if orientation == "vertical":
            rows_to_check = range(boat_row - 1, boat_row + ship_len + 1)
            cols_to_check = range(boat_column - 1, boat_column + 2)
        elif orientation == "horizontal":
            rows_to_check = range(boat_row - 1, boat_row + 2)
            cols_to_check = range(boat_column - 1, boat_column + ship_len + 1)
        else:
            return False  # Invalid orientation

        for row in rows_to_check:
            for col in cols_to_check:
                if (
                    row < 0
                    or row >= len(self.__boatfield)
                    or col < 0
                    or col >= len(self.__boatfield[0])
                ):
                    continue  # Ignore out-of-bounds cells
                if self.__boatfield[row][col] == 1:
                    print(
                        "Not an allowed position. Your wanted boat is too close or crossing another one!"
                    )
                    return False

        return True

    def set_ship(self, ship_len, ship_type, is_bot):
        """
        Asks the player for the start location and direction of a ship of the given length and sets it on the game field.
        """
        while True:
            # ask start location
            start_row, start_col = self.__get_row_and_column_input(
                "Enter the start position for your ship (e.g. A1): ", is_bot
            )
            if not is_bot:
                print("Enter the direction for your ship. Use your arrow Keys!")
                direction = get_arrow_key()
            else:
                match int(random.randint(0, 3)):
                    case 0:
                        direction = "up"
                    case 1:
                        direction = "down"
                    case 2:
                        direction = "left"
                    case 3:
                        direction = "right"
                    case _:
                        direction = "Unknown direction"

            # Bei up bzw left wird der Startpunkt zu boat_row bzw boat_column zu dem oberen bzw. linken punkt umgesetzt
            if direction == "up":
                boat_column = start_col
                boat_row = start_row - (ship_len - 1)
                orientation = "vertical"
            elif direction == "down":
                boat_column = start_col
                boat_row = start_row
                orientation = "vertical"
            elif direction == "left":
                boat_column = start_col - (ship_len - 1)
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
            # Is needed to reliably check if the Boat fits on the board
            # pylint: disable=too-many-boolean-expressions
            if (
                (orientation == "vertical" and (boat_row + ship_len) > self.__fsize)
                or (
                    orientation == "horizontal"
                    and (boat_column + ship_len) > self.__fsize
                )
                or boat_row < 0
                or boat_column < 0
            ):
                print(
                    "Ship does not fit on the board. Please choose a different start position or direction."
                )
                continue
            # pylint: enable=too-many-boolean-expressions

            valid = self.__check_ship_surrounding(
                orientation, ship_len, boat_row, boat_column
            )
            if valid:
                break

        # Boot in Feld plazieren Entweder von oben nach unten, oder von links nach recht
        ship_position = []
        for i in range(ship_len):
            row = boat_row + i if orientation == "vertical" else boat_row
            col = boat_column if orientation == "vertical" else boat_column + i

            self.__boatfield[row][col] = 1
            ship_position.append([row, col])
        self.owner.add_ship(ship_type, ship_position)

    def attack_enemy(self, target):
        """
        Attacks the enemy's boat at the specified position.
        """
        if self == target:
            raise ValueError("You cannot attack yourself!")

        if target.owner.get_ship_amount() == 0:
            print(f"Congrats {self.owner.get_player_name()}, YOU WON!")
            return 0

        # If the player is a bot, randomly choose a position that has not been used before to attack
        bot = self.owner.get_bot()
        if bot:
            while True:
                row, col = self.__get_row_and_column_input("Bot", bot)

                if [col, row] not in self.__botcache:
                    self.__botcache.append([col, row])
                    break
        # Otherwise, prompt the player to choose a position to attack
        else:
            row, col = self.__get_row_and_column_input(
                "Enter the attacking position for your ship (e.g. A1): ", bot
            )

        # Check if the attack hits a ship or not
        # And if it hits a ship, the player gets to attack again
        if target.get_boatfield()[row][col] == 1:
            print("Sir, we hitted an enemy target!")

            self.set_hitfield_cell(row, col, 1)
            target.set_boatfield_cell(row, col, "X")
            target.owner.ships_after_attack([row, col])

            if target.owner.get_ship_amount() == 0:
                print(f"Congrats {self.owner.get_player_name()}, YOU WON!")
                return 0

            print("You can attack a second time")
            return 1
            return self.attack_enemy(target)

        elif target.get_boatfield()[row][col] == "X":
            print("We already hit this Part")
        else:
            print("Sir we've hit the bull's eye!")
            self.set_hitfield_cell(row, col, "o")

        return 2
