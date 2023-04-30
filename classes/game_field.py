"""
The GameField class represents the game board and handles most game logic.
"""
from string import ascii_uppercase
import time
import random

from library import keyboard_helper
from library import console_helper


class GameField:
    """
    This class defines the game field, which holds information about ships positions and shots in the game.
    It has several methods to display the field and modify the field with the addition of ships and shots.
    """

    def __init__(self, owner, matrix_size=10):
        random.seed(time.time())
        self.owner = owner
        self.__fsize = matrix_size
        self.__boatfield = self.init_field()
        self.__hitfield = self.init_field()

    # getter
    def get_boatfield(self):
        """Returns the boatfield matrix."""
        return self.__boatfield

    def get_hitfield(self):
        """Returns the hitfield matrix."""
        return self.__hitfield

    def get_matrix_size(self):
        """Gets the matrix size variable"""
        return self.__fsize

    # init
    def init_field(self):
        """Returning the starter field Matrix"""
        return [[0 * i for j in range(self.__fsize)] for i in range(self.__fsize)]

    # setter
    def set_matrix_size(self, value):
        """Sets the matrix size variable"""
        self.__fsize = value

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

    # Show Field Functions
    def __get_field_text(self, fieldtype):
        """
        Returns string of Field with colorized Postion Indictaros at the top and left, like A1, B10, etc.
        """

        # Set Uppersite Alphabet
        txt = " " * (len(str(self.__fsize)) + 2)
        for elem in range(self.__fsize):
            txt += (
                f"{console_helper.BROWN}{ascii_uppercase[elem]}{console_helper.RESET} "
            )
        txt += "\n"

        # Set complete matrix with Linenumbers at the side
        for num, line in enumerate(fieldtype, 1):
            txt += f"{console_helper.BROWN}{num}{console_helper.RESET}   "
            if len(str(num)) > 1:
                txt += "\b" * (len(str(num)) - 1)
            for row in line:
                if row == 1:
                    color = console_helper.DARK_GRAY
                    row = "■"
                elif row == "X":
                    color = console_helper.RED
                    row = "■"
                elif row == "o":
                    color = console_helper.LIGHT_GREEN
                else:
                    color = console_helper.BLUE
                    row = "~"
                txt += color + str(row) + " "
            txt += console_helper.RESET + "\n"
        txt += console_helper.RESET
        return txt

    def show_boatfield(self):
        """Prints the boatfield matrix."""
        print(self.__get_field_text(self.__boatfield))

    def show_hitfield(self):
        """Prints the hitfield matrix."""
        print(self.__get_field_text(self.__hitfield))

    def show_fields_side_by_side(self):
        """Prints the boatfield and the hitfield matrix side by side."""
        padding = 4
        # Add Fieldtypename
        print(
            console_helper.GREEN
            + "Boatfield"
            + " " * ((len(self.__boatfield) * 2) + padding - 1)
            + "Hitfield"
            + console_helper.RESET
        )

        console_helper.print_side_by_side(
            [
                f"{self.__get_field_text(self.__boatfield)}",
                f"{self.__get_field_text(self.__hitfield)}",
            ],
            padding=padding,
        )

    # Ship placement functions
    def __get_row_and_column_input(self, message, bot):
        """
        Gets the Field-Coordiantes the user puts in using the message given to it. input Either in A1 or 1A format
            - returns: row, column
        """

        l_row = ""
        l_col = ""

        while bot is False:
            keyboard_helper.clear_input()
            user_input = input(f"{message}").strip().replace(" ", "")

            try:
                # Input A1
                l_row = int(user_input[1:]) - 1
                l_col = int(ascii_uppercase.index(user_input[0].upper()))
            except ValueError:
                try:
                    # If the Array is three long, the Number in front might have two digits
                    if len(user_input) == 3:
                        l_row = int(user_input[:2]) - 1
                        l_col = int(ascii_uppercase.index(user_input[2:].upper()))
                    else:
                        l_row = int(user_input[0]) - 1
                        l_col = int(ascii_uppercase.index(user_input[1:].upper()))
                except (IndexError, InterruptedError, ValueError):
                    console_helper.refresh_console_lines(2)
                    print("Not a valid Input! Please try again!")
                    continue
            except (IndexError, InterruptedError):
                console_helper.refresh_console_lines(2)
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
                try:
                    if row < 0 or col < 0:
                        continue
                    if self.__boatfield[row][col] == 1:
                        console_helper.refresh_console_lines(4)
                        print(
                            "Not an allowed position. Your wanted boat is too close or crossing another one!"
                        )
                        return False
                except IndexError:
                    pass
        return True

    def __finish_set_ship(self, orientation, ship_len, ship_type, boat_pos):
        """
        Adding ship to boatfield and players ships-list
        """
        boat_row = boat_pos[0]
        boat_column = boat_pos[1]

        # Boot in Feld plazieren Entweder von oben nach unten, oder von links nach recht
        ship_position = []
        for i in range(ship_len):
            row = boat_row + i if orientation == "vertical" else boat_row
            col = boat_column if orientation == "vertical" else boat_column + i

            self.__boatfield[row][col] = 1
            ship_position.append([row, col])
        self.owner.add_ship(ship_type, ship_position)

    def set_ship(self, ship_len, ship_type, is_bot):
        """
        Asks the player for the start location and direction of a ship of the given length and places it on the game field.
        Returns a boolean if it was possible to set the ship after X iterations: (len(matrix)^2)*len(directions) * buffer
        """
        directions = ["up", "down", "left", "right"]

        # 10*10 Matrix * 4 direction * 1/4 buffer -> 500
        endless_index = ((self.__fsize * self.__fsize) * len(directions))
        endless_index += endless_index * (1 / 4)

        while True:
            endless_index -= 1

            if endless_index <= 0:
                # In this case it took too long to place the ship
                # It has a too high chance of a corrupted Field
                return False

            # ask start location
            start_row, start_col = self.__get_row_and_column_input(
                f"Enter the start position for your {console_helper.BROWN}{ship_type}{console_helper.RESET} (e.g. A1): ",
                is_bot
            )

            direction = ""
            if is_bot:
                direction = directions[random.randint(0, len(directions) - 1)]
            else:
                print("Enter the direction for your ship. Use your arrow Keys!")
                direction = keyboard_helper.get_arrow_key()

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
            # print(direction)

            # check if ship fits on the board

            # This pylint entry is needed to reliably check if the Boat fits on the board!
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

        # ending set_ship by adding ship to boatfield and owners ship list
        self.__finish_set_ship(
            orientation, ship_len, ship_type, (boat_row, boat_column)
        )
        return True

    def attack_enemy(self, target):
        """
        Attacks the enemy's boat at the specified position.
        """

        if self == target:
            raise ValueError("You cannot attack yourself!")

        if target.owner.get_ship_amount() == 0:
            print(
                f"{console_helper.RED}Congrats {self.owner.get_player_name()}, YOU WON!{console_helper.RESET}"
            )
            return 0

        # If the player is a bot, randomly choose a position that has not been used before to attack
        bot = self.owner.get_bot()
        if bot:
            while True:
                row, col = self.__get_row_and_column_input("Bot", bot)
                botcache = self.owner.get_botcache()

                if [col, row] not in botcache:
                    botcache.append([col, row])
                    self.owner.set_botcache(botcache)
                    break
        # Otherwise, prompt the player to choose a position to attack
        else:
            row, col = self.__get_row_and_column_input(
                "Enter the attacking position for your ship (e.g. A1): ", bot
            )

        # Check if the attack hits a ship or not
        # And if it hits a ship return "hit" so the player gets to attack again
        if target.get_boatfield()[row][col] == 1:
            self.set_hitfield_cell(row, col, "X")
            target.set_boatfield_cell(row, col, "X")
            console_helper.clear_console()
            target.owner.ships_after_attack([row, col])

            if target.owner.get_ship_amount() == 0:
                print(
                    f"{console_helper.LIGHT_RED}Congrats {self.owner.get_player_name()}, YOU WON!{console_helper.RESET}"
                )
                return "win"

            if bot is False:
                self.show_fields_side_by_side()
            print(
                f"Sir, we hitted an enemy target at {console_helper.BROWN}{ascii_uppercase[col]}{row + 1}{console_helper.RESET}!"
            )

            print("You can attack a second time")
            return "hit"

        if target.get_boatfield()[row][col] == ("X" or "o"):
            print("We already hit this Part")
        else:
            print("Sir we've hit the bull's eye!")
            self.set_hitfield_cell(row, col, "o")

        return "water"
