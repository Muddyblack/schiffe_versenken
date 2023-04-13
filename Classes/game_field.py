from string import ascii_uppercase
from datetime import datetime
import random
import msvcrt
import time


class GameField:
    def __init__(self, bot=False):
        random.seed(datetime.now().timestamp())

        self.__fsize = 10
        self.__hitfield = [
            [0 * i for j in range(self.__fsize)] for i in range(self.__fsize)
        ]
        self.__boatfield = self.__hitfield

        self.__bot = bot
        self.__botcache = []
        self.__ships = 10

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
                print(row, end=" ")
            print("")

    def show_boatfield(self):
        self.show_field(self.__boatfield)

    def show_hitfield(self):
        self.show_field(self.__hitfield)

    # getter
    def get_ships(self):
        return self.__ships

    def get_bot(self):
        return self.__bot

    def get_boatfield(self):
        return self.__boatfield

    def get_hitfield(self):
        return self.__hitfield

    # setter
    def set_boatfield(self, row, col, value=0):
        self.__boatfield[row][col] = value

    def set_ship(self, shiplength):
        # asks startlocation and direction via arrows
        # check not over field size and not already set

        placed = False
        while not placed:
            # ask start location
            start_pos = input("Enter the start position for your ship (e.g. A1): ")
            try:
                start_col = ascii_uppercase.index(start_pos[0])
                start_row = int(start_pos[1:]) - 1
            except Exception:
                continue

            print("Enter the direction for your ship. Use your arrow Keys!")
            while True:
                arrow = ""

                if msvcrt.kbhit():
                    key = msvcrt.getch()

                    if key == b"\x00":
                        arrow = msvcrt.getch()
                    if arrow == b"H":
                        direction = "up"
                        end_col = start_col
                        end_row = start_row - (shiplength - 1)

                    elif arrow == b"P":
                        direction = "down"
                        end_col = start_col
                        end_row = start_row + (shiplength - 1)

                    elif arrow == b"K":
                        direction = "left"
                        end_col = start_col - (shiplength - 1)
                        end_row = start_row

                    elif arrow == b"M":
                        direction = "right"
                        end_col = start_col + (shiplength - 1)
                        end_row = start_row

                    else:
                        print("Invalid direction")
                        continue
                    print(f"{direction} arrow key pressed")
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

            # check if ship overlaps with other ships and place ship on board
            overlap = False
            temp_boatfield = self.__boatfield

            for i in range(shiplength):
                if direction == "up":
                    if self.__boatfield[start_row - i][start_col] == 0:
                        temp_boatfield[start_row - i][start_col] = 1
                elif direction == "down":
                    if self.__boatfield[start_row + i][start_col] == 0:
                        temp_boatfield[start_row + i][start_col] = 1
                elif direction == "left":
                    if self.__boatfield[start_row][start_col - i] == 0:
                        temp_boatfield[start_row][start_col - i] = 1
                elif direction == "right":
                    if self.__boatfield[start_row][start_col + i] == 0:
                        temp_boatfield[start_row][start_col + i] = 1
                else:
                    overlap = True
                    break

            if overlap:
                print(
                    "Ship overlaps with another ship. Please choose a different start position or direction."
                )
                continue

            self.__boatfield = temp_boatfield
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
                pos = input("Enter the start position for your ship (e.g. A1): ")
                try:
                    col = ascii_uppercase.index(pos[0])
                    row = int(pos[1:]) - 1
                except Exception:
                    continue

        print(target.get_boatfield())
        print(row, col)
        if target.get_boatfield()[row][col] == 1:
            print("Sir, we hitted an enemy target!")
            self.__hitfield[row][col] = 1
            target.set_boatfield(row, col, "X")
            self.attack_enemy(target)
        elif target.get_boatfield()[row][col] == "X":
            print("We already hit this Part")
        else:
            print("Sir we've hit the bull's eye!")


if __name__ == "__main__":
    s1 = GameField(True)
    s1.show_boatfield()
    s1.show_boatfield()

    s2 = GameField()
    s2.set_ship(5)
    while True:
        s1.attack_enemy(s2)
        s1.show_hitfield()
        s2.show_boatfield()
        time.sleep(1)
