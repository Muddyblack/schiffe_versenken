import os
import gc
import pickle
from Classes import game_field
import keyboard

project_path = f"{os.path.abspath(os.path.dirname(os.path.realpath(__file__)))}"
save_game_path = f"{project_path}\\Saving"


def clear_previous_console_output():
    os.system("cls" if os.name == "nt" else "clear")


def place_all_ships(player):
    # Regelt das plazieren aller Boote.
    battleship = 1
    cruiser = 2
    destroyer = 3
    uboat = 4
    while (battleship + cruiser + destroyer + uboat) != 0:
        player.show_boatfield()
        print(
            f"You have {battleship} Battleship (5-Long), {cruiser} Cruiser (4-Long), {destroyer} Destroyer (3-Long)"
            f" and {uboat} U-Boats (2-Long) availible!\nWhich Ship would you like to place?"
        )
        current_boat_to_place = str(
            input("Please type in the boats name, or the length of it: ")
        )
        current_boat_to_place.lower()

        match current_boat_to_place:
            case "2" | "u-boat" | "uboat":
                if uboat > 0:
                    player.set_ship(2)
                    uboat -= 1
                else:
                    print("You already placed all your U-Boats!")
            case "3" | "destroyer":
                if destroyer > 0:
                    player.set_ship(3)
                    destroyer -= 1
                else:
                    print("You already placed all your Destroyers!")
            case "4" | "cruiser":
                if cruiser > 0:
                    player.set_ship(4)
                    cruiser -= 1
                else:
                    print("You already placed all your Cruisers!")
            case "5" | "battleship":
                if battleship > 0:
                    player.set_ship(5)
                    battleship -= 1
                else:
                    print("You already placed your Battleship!")
            case _:
                clear_previous_console_output()
                print("Unknown Boat-Type.")

    input(
        "You placed all your Boats! Your final Field looks like this. Press Enter to Continue!"
    )
    player.show_boatfield()


def save_game():
    player_list = []

    for player in gc.get_objects():
        if isinstance(player, game_field.GameField):
            player_info = {
                "name": player.get_player_name(),
                "bot": player.get_bot(),
                "boatfield": player.get_boatfield(),
                "hitfield": player.get_hitfield(),
            }
            player_list.append(player_info)

    with open(f"{save_game_path}\game_save.pkl", "wb") as playerpickle:
        pickle.dump(player_list, playerpickle)


def select_savegame(save_games):
    # Set up the initial selected save game index to 0
    selected_save_game_index = 0

    # Display the list of save games with the currently selected save game highlighted
    def display_save_games():
        for i, j in enumerate(save_games):
            if i == selected_save_game_index:
                print(f"> {save_games[i]}")
            else:
                print(f"  {save_games[i]}")

    display_save_games()

    while True:
        # Handle arrow key presses to move the selected save game index up or down
        if keyboard.is_pressed("up") and selected_save_game_index > 0:
            selected_save_game_index -= 1
            display_save_games()
            while keyboard.is_pressed("up"):
                pass
        elif (
            keyboard.is_pressed("down")
            and selected_save_game_index < len(save_games) - 1
        ):
            selected_save_game_index += 1
            display_save_games()
            while keyboard.is_pressed("down"):
                pass

        # Handle enter key press to select the currently highlighted save game
        elif keyboard.is_pressed("enter"):
            break

    # The selected save game index can now be used to load the corresponding save game
    print("Selected save game index:", selected_save_game_index)


def start_up():
    what_to_load = ""
    exist_game_saves = []

    for file in os.listdir(f"{save_game_path}"):
        if file.endswith(".pkl"):
            exist_game_saves.append(os.path.join(save_game_path, file))

    if len(exist_game_saves) != 0:
        what_to_load = "n"

    while what_to_load != ("y" or "n"):
        what_to_load = input("Do you want to load an old save? [y/n]: ").lower()

    if what_to_load == "y":
        select_savegame(exist_game_saves)

        with open(f"{project_path}\\Saving\\game_save.pkl", "rb") as playerpickle:
            player_list = pickle.load(playerpickle)
            print(player_list)
    else:
        pass


if __name__ == "__main__":
    s1 = game_field.GameField(name="Buckki")
    s2 = game_field.GameField(bot=True)

    clear_previous_console_output()
    # Player 1 place ships.
    start_up()
    place_all_ships(s1)
    # save_game()
    """

    while s1.get_ships_left() != 0 | s2.get_ships_left() != 0:
        s1.attack_enemy(s2)
        s1.show_hitfield()
        s2.show_boatfield()
    """
