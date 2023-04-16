from string import ascii_uppercase
from datetime import datetime
import random
import keyboard

# anicode
BLUE = "\033[0;34m"
RED = "\033[0;31m"
RESET = "\033[0m"


class GameField:
    def __init__(self, bot=False, name="Player"):
        random.seed(datetime.now().timestamp())

        self.__fsize = 10
        self.__ships = 10
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

    # Print Field with Postion Indictaros at the top and left, like A1, B10, etc to the Command-Line
    def show_field(self, fieldtype):
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
    def get_ships_left(self):
        return self.__ships

    def get_bot(self):
        return self.__bot

    def get_boatfield(self):
        return self.__boatfield

    def get_hitfield(self):
        return self.__hitfield

    def get_player_name(self):
        return self.__player_name

    def get_current_Turn(self):
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

    def set_current_Turn(self, value):
        self.__current_turn = value

    def set_ship(self, shiplength):
        # asks startlocation and direction via arrows
        # check not over field size and not already set

        placed = False
        while not placed:
            # ask start location
            start_pos = input(
                f"Enter the start position for your ship {shiplength} long ship (e.g. A1): "
            )
            try:
                start_col = ascii_uppercase.index(start_pos[0])
                start_row = int(start_pos[1:]) - 1
            except Exception:
                continue

            print("Enter the direction for your ship. Use your arrow Keys!")
            while True:
                if keyboard.is_pressed("up"):
                    direction = "up"
                    end_col = start_col
                    end_row = start_row - (shiplength - 1)
                    while keyboard.is_pressed("up"):
                        pass

                elif keyboard.is_pressed("down"):
                    direction = "down"
                    end_col = start_col
                    end_row = start_row + (shiplength - 1)
                    while keyboard.is_pressed("down"):
                        pass

                elif keyboard.is_pressed("left"):
                    direction = "left"
                    end_col = start_col - (shiplength - 1)
                    end_row = start_row
                    while keyboard.is_pressed("left"):
                        pass

                elif keyboard.is_pressed("right"):
                    direction = "right"
                    end_col = start_col + (shiplength - 1)
                    end_row = start_row
                    while keyboard.is_pressed("right"):
                        pass

                elif keyboard.read_key() != "":
                    print("Invalid direction")
                    continue
                break

            # check if ship fits on the board
            if (
                end_col >= self.__fsize
                or end_col < 0
                or end_row >= self.__fsize
                or end_row < 0
            ):
                print(
                    "Ship does not fit on the board. Please choose a different start position or direction."
                )
                continue

            # Bei up und down ist start und end_col gleich
            # Bei right and left ist start und end_row gleich
            if direction == "up":
                boat_column = start_col
                boat_row_top = end_row
                orientation = "vertical"
            elif direction == "down":
                boat_column = start_col
                boat_row_top = start_row
                orientation = "vertical"
            elif direction == "right":
                boat_row = start_row
                boat_column_left = start_col
                orientation = "horizontal"
            elif direction == "left":
                boat_row = start_row
                boat_column_left = end_col
                orientation = "horizontal"
            else:
                print("Direction Error!")

            valid = True
            # Check for neighboring ships
            if orientation == "vertical":
                for i in range(-1, 1):
                    for j in range(shiplength + 2):
                        checkfield = self.__boatfield[boat_row_top - 1 + j][
                            boat_column + i
                        ]
                        if checkfield == 1 and valid:
                            print(
                                "Not an allowed position. Your wantedBoat is too close or crossing another one!"
                            )
                            valid = False
            elif orientation == "horizontal":
                for i in range(-1, 1):
                    for j in range(shiplength + 2):
                        checkfield = self.__boatfield[boat_row + i][
                            boat_column_left - 1 + j
                        ]
                        if checkfield == 1 and valid:
                            print(
                                "Not an allowed position. Your wanted Boat is too close or crossing another one!"
                            )
                            valid = False

            if valid:
                # Boot in Feld plazieren Entweder von oben nach unten, oder von links nach recht
                if orientation == "vertical":
                    for i in range(shiplength):
                        self.__boatfield[boat_row_top + i][boat_column] = 1
                elif orientation == "horizontal":
                    for i in range(shiplength):
                        self.__boatfield[boat_row][boat_column_left + i] = 1
                placed = True

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
                except Exception:
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
