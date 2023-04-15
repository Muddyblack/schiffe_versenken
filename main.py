import os
from Classes import game_field

project_path = f"{os.path.dirname(os.path.abspath(__file__))}"


def clear_previous_console_output():
    os.system("cls" if os.name == "nt" else "clear")


def place_all_ships(player):
    # Regelt das plazieren aller Boote.
    battleship = 1
    cruiser = 2
    destroyer = 3
    uboat = 4
    while battleship and cruiser and destroyer and uboat != 0:
        player.show_boatfield()
        print(f"You have {battleship} Battleship (5-Long), {cruiser} Cruiser (4-Long), {destroyer} Destroyer (3-Long)"
              f" and {uboat} U-Boats (2-Long) availible!\nWhich Ship would you like to place?")
        current_boat_to_place = str(input("Please type in the boats name, or the length of it: "))
        current_boat_to_place.lower()

        match current_boat_to_place:
            case '2' | 'u-boat' | 'uboat':
                if uboat > 0:
                    player.set_ship(2)
                    uboat -= 1
                else:
                    print("You already placed all your U-Boats!")
            case '3' | 'destroyer':
                if destroyer > 0:
                    player.set_ship(3)
                    destroyer -= 1
                else:
                    print("You already placed all your Destroyers!")
            case '4' | 'cruiser':
                if cruiser > 0:
                    player.set_ship(4)
                    cruiser -= 1
                else:
                    print("You already placed all your Cruisers!")
            case '5' | 'battleship':
                if battleship > 0:
                    player.set_ship(5)
                    battleship -= 1
                else:
                    print("You already placed your Battleship!")
            case _:
                print("Unknown Boat-Type.")

    input("You placed all your Boats! Your final Field looks like this. Press Enter to Continue!")
    player.show_boatfield()


if __name__ == "__main__":
    s1 = game_field.GameField(False)
    s2 = game_field.GameField(True)

    # Player 1 place ships.
    place_all_ships(s1)

    while s1.get_ships_left() != 0 | s2.get_ships_left() != 0:
        s1.attack_enemy(s2)
        s1.show_hitfield()
        s2.show_boatfield()
