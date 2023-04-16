"""This is the main module where the entire game logic gets merged"""
import os
import sys
import gc
import pickle
import random
import keyboard
from Classes import game_field

#
PROJECT_PATH = f"{os.path.abspath(os.path.dirname(os.path.realpath(__file__)))}"
GAME_DATA_PATH = f"{PROJECT_PATH}/GameData"
SAVE_GAMES_PATH = f"{GAME_DATA_PATH}/saves"

os.makedirs(SAVE_GAMES_PATH, exist_ok=True)

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


def clear_console():
    """clearing the console"""
    os.system("cls" if os.name == "nt" else "clear")


def place_all_ships(obj):
    """Regelt das plazieren aller Boote."""
    battleship = 1
    cruiser = 2
    destroyer = 3
    uboat = 4
    while (battleship + cruiser + destroyer + uboat) != 0:
        obj.show_boatfield()
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
                    obj.set_ship(2)
                    uboat -= 1
                else:
                    print("You already placed all your U-Boats!")
            case "3" | "destroyer":
                if destroyer > 0:
                    obj.set_ship(3)
                    destroyer -= 1
                else:
                    print("You already placed all your Destroyers!")
            case "4" | "cruiser":
                if cruiser > 0:
                    obj.set_ship(4)
                    cruiser -= 1
                else:
                    print("You already placed all your Cruisers!")
            case "5" | "battleship":
                if battleship > 0:
                    obj.set_ship(5)
                    battleship -= 1
                else:
                    print("You already placed your Battleship!")
            case _:
                clear_console()
                print(f"{BOLD}{RED}Unknown Boat-Type.{RESET}")

    input(
        "You placed all your Boats! Your final Field looks like this. Press Enter to Continue!"
    )
    obj.show_boatfield()


def save_game(save_name):
    """Saves the current state of the game in a binary file format."""
    player_list = []

    for obj in gc.get_objects():
        if isinstance(obj, game_field.GameField):
            player_info = {
                "name": obj.get_player_name(),
                "bot": obj.get_bot(),
                "boatfield": obj.get_boatfield(),
                "hitfield": obj.get_hitfield(),
                "current_turn": obj.get_current_turn(),
            }
            player_list.append(player_info)

    save_dir = f"{SAVE_GAMES_PATH}/{save_name}"
    os.makedirs(save_dir, exist_ok=True)

    with open(f"{save_dir}/players.obj", "wb") as obj:
        pickle.dump(player_list, obj)


def refresh_console_lines(lines):
    """Clears the specified number of lines from the console output."""

    sys.stdout.write("\033[K" * lines)
    sys.stdout.write("\033[F" * lines)


def display_save_games(save_games, selected_save_game_index):
    """DisplayS the list of save games with the currently selected save game highlighted"""

    for i in enumerate(save_games):
        game_name = os.path.basename(save_games[i[0]])
        if i[0] == selected_save_game_index:
            print(f"{CYAN}> {game_name}{RESET}")
        else:
            print(f"  {game_name}")


def select_savegame(save_games):
    """
    Allows the user to select a saved game from a list of saved game directories displayed on the console.
    The user uses arrow-keys and the enter-key

    Returns:
        - (str): The selected game directory.
    """
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
    """Prints a beautiful ASCII-Logo for the game to the console"""
    print(
        rf"""{MAGENTA}
    _           _   _   _           _     _       
   | |         | | | | | |         | |   (_)      
   | |__   __ _| |_| |_| | ___  ___| |__  _ _ __  
   | '_ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \ 
   | |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) |
   |_.__/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ 
                                           | |    
                                           |_|    
                                   {BROWN}
    {LIGHT_GRAY}
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


def ask_name():
    """
    Asks the user to enter his name and checks if it is not empty or longer than 15 characters
    Returns:
        -(str): name
    """
    min_name_len = 3
    max_name_len = 15

    while True:
        name = input("\nNice, so what is your name: ").strip()

        if name == "":
            msg = "This is just an empty String!"
        elif len(name) > max_name_len:
            msg = "The name is too long it has: {len(name)} character allowed: {max_name_len}"
        elif len(name) <= min_name_len:
            msg = "The name is too short it has: {len(name)} min length: {min_name_len}"
        else:
            break

        print(msg)

    return name


def start_up():
    """
    Sets up the initial game environment
    If the user chooses to load an old save, it loads the save game and returns the GameField instances for both players.
    Otherwise, it asks for the player's name, whether they want to play against a real person or a bot, and starts the game
    by randomly choosing which player goes first.

    Returns:
        A dictionary with keys "players" and "save_name". The value for the key "players" is a list of two GameField instances
        representing the players. The value for the key "save_name" is a string representing the name of the save game.
    """
    start_screen()
    p_1 = None
    p_2 = None
    save_name = ""

    load = ""
    exist_game_saves = [
        f.name
        for f in os.scandir(SAVE_GAMES_PATH)
        if f.is_dir() and not f.is_file() and "_save" in f.name
    ]

    if len(exist_game_saves) == 0:
        load = "n"

    while load not in ("y", "n"):
        load = input("Do you want to load an old save? [y/n]: ").lower().strip()

    if load == "y":
        save_name = select_savegame(exist_game_saves)

        with open(f"{SAVE_GAMES_PATH}/{save_name}/players.obj", "rb") as playerpickle:
            player_list = pickle.load(playerpickle)

        player_1 = player_list[0]
        player_2 = player_list[1]

        p_1 = game_field.GameField(name=player_1["name"], bot=player_1["bot"])
        p_1.set_current_turn(player_1["current_turn"])
        p_1.set_boatfield(player_1["boatfield"])
        p_1.set_hitfield(player_1["hitfield"])

        p_2 = game_field.GameField(name=player_2["name"], bot=player_2["bot"])
        p_2.set_current_turn(player_2["current_turn"])
        p_2.set_boatfield(player_2["boatfield"])
        p_2.set_hitfield(player_2["hitfield"])

    else:
        print("Hello you decided to create a new Save-game")
        save_name = (
            f'{input("    Enter the save-name you wish here: ").replace(" ", "_")}_save'
        )
        opponent = ""

        p1_name = ask_name()
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
            while True:
                p2_name = ask_name()
                if p2_name != p1_name:
                    break
                print("The other player has already this name!")
            p_2 = game_field.GameField(name=p2_name)
        else:
            p_2 = game_field.GameField(bot=True)

        # Coin flipping who will start the Game
        starter = random.randint(0, 1)
        if starter == 0:
            p_1.set_current_turn(True)
        else:
            p_2.set_current_turn(True)

    return {"players": [p_1, p_2], "save_name": save_name}


if __name__ == "__main__":
    start = start_up()
    players = start["players"]
    save = start["save_name"]

    for player in players:
        if player.get_current_turn() is False:
            continue

        print(f"TEST: HELLO {player.get_player_name()} it should be your turn")
        break

    # p_1 = start[0]
    # p_2 = start[1]
    # save = "salbana"  # start[2]
    # p_1 = game_field.GameField("Pette", False)
    save_game(save)

    # place_all_ships(p_1)
    # place_all_ships(p_2)

    # p_1.show_boatfield()
    # p_2.show_boatfield()

    # while p_1.get_ships_left() != 0 | p_2.get_ships_left() != 0:
    #    p_1.attack_enemy(p_2)
    #    p_1.show_hitfield()
    #    p_2.show_boatfield()
    # save_game(save_name)
