import os
import sys
import gc
import pickle
import keyboard
from Classes import game_field
from Library.anicodes import *


project_path = f"{os.path.abspath(os.path.dirname(os.path.realpath(__file__)))}"
save_game_path = f"{project_path}\\Saving"

# enables ansi escape characters in terminal
os.system("")
# Define color codes for ANSI escape sequences
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
MAGENTA = "\033[35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
RESET = "\033[0m"


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
                print(f"{BOLD}{RED}Unknown Boat-Type.{RESET}")

    input(
        "You placed all your Boats! Your final Field looks like this. Press Enter to Continue!"
    )
    player.show_boatfield()


def save_game(save_name):
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

    with open(f"{save_name.replace('.pkl', '')}.pkl", "wb") as playerpickle:
        pickle.dump(player_list, playerpickle)


def refresh_console_lines(lines):
    sys.stdout.write("\033[K" * lines)
    sys.stdout.write("\033[F" * lines)


def display_save_games(save_games, selected_save_game_index):
    # Display the list of save games with the currently selected save game highlighter

    for i in enumerate(save_games):
        game_name = os.path.basename(save_games[i[0]])
        if i[0] == selected_save_game_index:
            print(f"{CYAN}> {game_name}{RESET}")
        else:
            print(f"  {game_name}")


def select_savegame(save_games):
    # Selecting Savegame with arrow-keys and with hitting enter
    # returns the selected game directory
    selected_save_game_index = 0
    save_games_len = len(save_games)

    display_save_games(save_games, selected_save_game_index)

    while True:
        # Handle arrow key presses to move the selected save game index up or down

        if keyboard.is_pressed("up") and selected_save_game_index > 0:
            selected_save_game_index -= 1
            refresh_console_lines(save_games_len)
            display_save_games(save_games, selected_save_game_index)

            while keyboard.is_pressed("up"):
                pass

        elif (
            keyboard.is_pressed("down")
            and selected_save_game_index < len(save_games) - 1
        ):
            selected_save_game_index += 1
            refresh_console_lines(save_games_len)
            display_save_games(save_games, selected_save_game_index)

            while keyboard.is_pressed("down"):
                pass

        elif keyboard.is_pressed("enter"):
            break

    selected = save_games[selected_save_game_index]
    print(f"Selected save game: {os.path.basename(selected)}\n")
    return selected


def start_screen():
    print(
        rf"""{MAGENTA}
    _           _   _   _           _     _       
   | |         | | | | | |         | |   (_)      
   | |__   __ _| |_| |_| | ___  ___| |__  _ _ __  
   | '_ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \ 
   | |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) |
   |_.__/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ 
                                        | |    
                                        |_|    {BROWN}
                                        """
        + f"{LIGHT_GRAY}"
        + """
                       _  _                 |-._
                    -         - _           |-._|
                 O                 (). _    |
                                     '(_) __|__
                                     [__|__|_|_]
  ~~ _|_ _|_ _|_  ~~     ~~~          |__|__|_|
   __ |   |   |       ~~      ~~~     |_|__|__|
   HH_|___|___|__.--"  ~~~ ~~        /|__|__|_|
  |__________.-"     ~~~~    ~~~    / |_|__|__|
  ~     ~~ ~      ~~       ~~      /  |_| |___|
     ~~~~    ~~~   ~~~~   ~   ~~  /    
    jrei{RESET}
    """
    )


def start_up():
    start_screen()
    p_1 = None
    p_2 = None
    save_name = ""

    load = ""
    exist_game_saves = []

    for file in os.listdir(f"{save_game_path}"):
        if file.endswith(".pkl"):
            exist_game_saves.append(os.path.join(save_game_path, file))

    if len(exist_game_saves) == 0:
        load = "n"

    while load not in ("y", "n"):
        load = input("Do you want to load an old save? [y/n]: ").lower().strip()

    if load == "y":
        save_name = select_savegame(exist_game_saves)

        with open(save_name, "rb") as playerpickle:
            player_list = pickle.load(playerpickle)

        player_1 = player_list[0]
        player_2 = player_list[1]

        p_1 = game_field.GameField(player_1["name"], player_1["bot"])
        p_1.set_boatfield(player_1["boatfield"])
        p_1.set_hitfield(player_1["hitfield"])

        p_2 = game_field.GameField(player_2["name"], player_2["bot"])
        p_2.set_boatfield(player_2["boatfield"])
        p_2.set_hitfield(player_2["hitfield"])

    else:
        print("Hello you decided to create a new Save-game")
        save_name = f'{save_game_path}\\{input("    Enter the save-name you wish here: ").replace(" ", "_")}'
        opponent = ""

        p1_name = input("\nNice, so what is your name: ")
        while opponent not in ("y", "n"):
            opponent = (
                input(
                    f"Hello, {p1_name} would you like to play against a real person? [y/n]"
                )
                .lower()
                .strip()
            )

        p_1 = game_field.GameField(name=p1_name)

        if opponent == "y":
            opponent = input("Hey what is your name?")
            p_2 = game_field.GameField(name=opponent)
        else:
            p_2 = game_field.GameField(bot=True)

    return p_1, p_2, save_name


if __name__ == "__main__":
    start_screen()
    # start = start_up()

    # p_1 = start[0]
    # p_2 = start[1]
    # save_name = start[2]

    # save_game(save_name)
    p_1 = game_field.GameField("Pette", False)
    place_all_ships(p_1)
    # place_all_ships(p_2)

    # p_1.show_boatfield()
    # p_2.show_boatfield()

    # while p_1.get_ships_left() != 0 | p_2.get_ships_left() != 0:
    #    p_1.attack_enemy(p_2)
    #    p_1.show_hitfield()
    #    p_2.show_boatfield()
    # save_game(save_name)
