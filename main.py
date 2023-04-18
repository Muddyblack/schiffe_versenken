"""This is the main module where the entire game logic gets merged"""
import os
import sys
import gc
import pickle
import random
import time
import keyboard
from Classes.game_field import GameField
from Classes.player import Player

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

# pylint: disable=wrong-import-position
from Library.file_helper import read_file
from Library.keyboard_helper import clear_input
from Library import sound_helper

# pylint: enable=wrong-import-position

# Paths
PROJECT_PATH = f"{os.path.abspath(os.path.dirname(os.path.realpath(__file__)))}"
GAME_DATA_PATH = f"{PROJECT_PATH}/GameData"
SAVE_GAMES_PATH = f"{GAME_DATA_PATH}/saves"
START_SCREEN_ANIMATION_PATH = f"{GAME_DATA_PATH}/start_screen_animation"
SOUND_PATH = f"{GAME_DATA_PATH}/sound"

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


# Game System funcs
def clear_console():
    """clearing the console"""
    os.system("cls" if os.name == "nt" else "clear")


def refresh_console_lines(lines):
    """Clears the specified number of lines from the console output."""

    sys.stdout.write("\033[F" * lines)
    sys.stdout.write("\033[K" * lines)


def start_screen():
    """Prints a beautiful ASCII-Logo for the game to the console"""
    # start_music_path = f"{SOUND_PATH}/Start-Screen.wav"

    # sound_process = sound_helper.start(start_music_path)

    files = [
        os.path.abspath(os.path.join(START_SCREEN_ANIMATION_PATH, file))
        for file in os.listdir(START_SCREEN_ANIMATION_PATH)
    ]
    frames = sorted(files)

    stop = False
    while stop is False:
        if (
            (keyboard.is_pressed("return"))
            or (keyboard.is_pressed("enter"))
            or (stop is True)
        ):
            stop = True
            break

        for frame in frames:
            string = read_file(frame)
            for line in string:
                if (
                    keyboard.is_pressed("return")
                    or (keyboard.is_pressed("enter"))
                    or (stop is True)
                ):
                    stop = True
                    break
                print(
                    line.replace("{BROWN}", BROWN)
                    .replace("{LIGHT_GRAY}", LIGHT_GRAY)
                    .replace("{MAGENTA}", MAGENTA)
                    .replace("{RESET}", RESET)
                )
            print(f"\n{LIGHT_BLUE}Hit the Enter Key, to continue{RESET}", end="")
            # Check while sleeping if enter has been entered
            ind = 0
            while ind in range(40):
                time.sleep(0.01)
                if (
                    keyboard.is_pressed("return") or (keyboard.is_pressed("enter"))
                ) is True or (stop is True):
                    stop = True
                    break
                ind += 1

            if stop is True:
                break

            clear_console()
    time.sleep(0.1)
    sound_helper.stop(sound_process)
    clear_input()
    clear_console()


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

    print("Use up and down arrows to navigate\nUse Spacebar to sleect the game")
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

        elif keyboard.is_pressed(" "):
            break

    selected = save_games[selected_save_game_index]
    print(f"Selected save game: {os.path.basename(selected)}\n")
    return selected


def ask_name(question):
    """
    Asks the user to enter his name and checks if it is not empty or longer than 15 characters
    Returns:
        -(str): name
    """
    min_name_len = 3
    max_name_len = 15

    while True:
        name = input(f"\n{question}").strip()

        if name == "":
            msg = "This is just an empty String!"
        elif len(name) > max_name_len:
            msg = f"The name is too long it has: {len(name)} character allowed: {max_name_len}"
        elif len(name) < min_name_len:
            msg = (
                f"The name is too short it has: {len(name)} min length: {min_name_len}"
            )
        else:
            break

        print(msg)

    return name


def load_game(save_name):
    """
    Loads a saved game.

    Returns:
        -(tuple): two GameField instances and dictionary with game-infos
    """
    with open(f"{SAVE_GAMES_PATH}/{save_name}/players.obj", "rb") as playerpickle:
        player_list = pickle.load(playerpickle)
    with open(f"{SAVE_GAMES_PATH}/{save_name}/game.info", "rb") as playerpickle:
        game_info = pickle.load(playerpickle)

    last_turn_player = game_info["last_turn_player"]
    level = game_info["level"]

    obj_1 = player_list[0]
    obj_2 = player_list[1]

    p_1 = Player(name=obj_1["name"], bot=obj_1["bot"])
    p_1.set_ships(obj_1["ships"])
    f_1 = GameField(p_1)
    f_1.set_boatfield(obj_1["boatfield"])
    f_1.set_hitfield(obj_1["hitfield"])

    p_2 = Player(name=obj_2["name"], bot=obj_2["bot"])
    p_2.set_ships(obj_2["ships"])
    f_2 = GameField(p_2)
    f_2.set_boatfield(obj_2["boatfield"])
    f_2.set_hitfield(obj_2["hitfield"])

    if last_turn_player == f_1.owner.get_player_name():
        fields = (f_1, f_2)
    elif last_turn_player == f_2.owner.get_player_name():
        fields = (f_2, f_1)
    else:
        # Coin flipping who will start the Game
        starter = random.randint(0, 1)
        if starter == 0:
            fields = (f_1, f_2)
        else:
            fields = (f_2, f_1)

    return {"players": fields, "save_name": save_name, "level": level}


def save_game(save_name, last_turn_player, level):
    """Saves the current state of the game in a binary file format."""
    player_list = []
    game_info = {
        "last_turn_player": last_turn_player.owner.get_player_name(),
        "level": level,
    }

    for obj in gc.get_objects():
        if isinstance(obj, GameField):
            player_info = {
                "name": obj.owner.get_player_name(),
                "bot": obj.owner.get_bot(),
                "ships": obj.owner.get_ships(),
                "boatfield": obj.get_boatfield(),
                "hitfield": obj.get_hitfield(),
            }
            player_list.append(player_info)

    save_dir = f"{SAVE_GAMES_PATH}/{save_name}"
    os.makedirs(save_dir, exist_ok=True)

    with open(f"{save_dir}/players.obj", "wb") as obj:
        pickle.dump(player_list, obj)
    with open(f"{save_dir}/game.info", "wb") as obj:
        pickle.dump(game_info, obj)


def create__new_game(existing_saves):
    """
    Creates a new game.

    Returns:
        - (tuple): two GameField instances and dictionary with game-infos
    """
    while True:
        print("Hello you decided to create a new Save-game")
        save_name = f'{ask_name("Enter the save name you wish to use: ").replace(" ", "_")}_save'

        if save_name in existing_saves:
            print("This name does already exist!")
        else:
            break

    opponent = ""

    p1_name = ask_name("Nice, so what is your name: ")
    while opponent not in ("y", "n"):
        opponent = (
            input(
                f"Hello, {p1_name}, would you like to play against a real person? [y/n] "
            )
            .lower()
            .strip()
        )

    f_1 = GameField(Player(name=p1_name))

    if opponent == "y":
        while True:
            p2_name = ask_name(
                f"Hello {p1_name} told me about you.\nWhat is your name: "
            )
            if p2_name != p1_name:
                break
            print("The other player already has this name!")
        f_2 = GameField(Player(name=p2_name))
    else:
        f_2 = GameField(Player(bot=True))

    # Coin flipping who will start the Game
    starter = random.randint(0, 1)
    if starter == 0:
        fields = (f_1, f_2)
    else:
        fields = (f_2, f_1)

    return {"players": fields, "save_name": save_name, "level": 0}


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
    exist_game_saves = [
        f.name
        for f in os.scandir(SAVE_GAMES_PATH)
        if f.is_dir() and not f.is_file() and "_save" in f.name
    ]

    load = ""
    if len(exist_game_saves) == 0:
        load = "n"

    while load not in ("y", "n"):
        load = input("Do you want to load an old save? [y/n]: ").lower().strip()
        clear_input()

    if load == "y":
        return load_game(select_savegame(exist_game_saves))

    return create__new_game(exist_game_saves)


# Gameplay funcs
def choose_random_ship():
    """Chooses a random ship and returns in stringname of the boat"""
    rand_ship = random.randint(0, 3)
    match rand_ship:
        case 0: chosen_ship = "battleship"
        case 1: chosen_ship = "cruiser"
        case 2: chosen_ship = "destroyer"
        case 3: chosen_ship = "uboat"
        case _: chosen_ship = "Unknown"
    return str(chosen_ship)


def place_all_ships(obj, save_g, curr_lvl):
    """Regelt das plazieren aller Boote."""

    ships = obj.owner.get_ships()

    battleship = 1 - len(ships["battleship"])
    cruiser = 2 - len(ships["cruiser"])
    destroyer = 3 - len(ships["destroyer"])
    uboat = 4 - len(ships["uboat"])

    while (battleship + cruiser + destroyer + uboat) != 0:
        is_bot = obj.owner.get_bot
        if is_bot is False:
            obj.show_boatfield()

            print(
                f"You have {battleship} Battleship (5-Long), {cruiser} Cruiser (4-Long), {destroyer} Destroyer (3-Long)"
                f" and {uboat} U-Boats (2-Long) availible!\nWhich Ship would you like to place?"
            )
            clear_input()
            current_boat_to_place = str(
                   input("Please type in the boats name, or the length of it: ")
            ).lower()
        else:
            # Hier Schiffe automatisch plazieren
            current_boat_to_place = choose_random_ship()

        match current_boat_to_place:
            case "2" | "u-boat" | "uboat":
                if uboat > 0:
                    obj.set_ship(2, "u-boat", is_bot)
                    uboat -= 1
                else:
                    print("You already placed all your U-Boats!")
            case "3" | "destroyer":
                if destroyer > 0:
                    obj.set_ship(3, "destroyer", is_bot)
                    destroyer -= 1
                else:
                    print("You already placed all your Destroyers!")
            case "4" | "cruiser":
                if cruiser > 0:
                    obj.set_ship(4, "cruiser", is_bot)
                    cruiser -= 1
                else:
                    print("You already placed all your Cruisers!")
            case "5" | "battleship":
                if battleship > 0:
                    obj.set_ship(5, "battleship", is_bot)
                    battleship -= 1
                else:
                    print("You already placed your Battleship!")
            case _:
                clear_console()
                print(f"{BOLD}{RED}Unknown Boat-Type.{RESET}")
        save_game(save_g, player, curr_lvl)

    clear_console()
    obj.show_boatfield()
    input(
        "You placed all your Boats! Your final Field looks like this. Press Enter to Continue!"
    )
    clear_console()


def attack_execution(attacker, target):
    """Attacks the target and set target as new current_player"""
    attacker.attack_enemy(target)
    attacker.show_hitfield()
    target.show_boatfield()
    input(
        "You finished your Attack! Your final Fields looks like this. Press Enter to Continue!"
    )


# Game walkthrough
if __name__ == "__main__":
    start = start_up()
    players = start["players"]
    save = start["save_name"]
    current_level = start["level"]

    if current_level == 0:
        for index, player in enumerate(players):
            clear_console()
            print(f"Your Turn {player.owner.get_player_name()}!")
            save_game(save, player, current_level)
            place_all_ships(player, save, current_level)
            player.show_boatfield()
            if index < len(players):
                save_game(save, players[index + 1], current_level)
            else:
                save_game(save, players[0], current_level)
        current_level += 1

    player_1 = players[0]
    player_2 = players[1]

    if current_level == 1:
        while (player_1.get_ships_left() != 0) and (player_2.get_ships_left() != 0):
            print(f"Your Turn {player_1.owner.get_player_name()}!")
            attack_execution(player_1, player_2)
            save_game(save, players[0], current_level)
            print(f"Your Turn {player_2.owner.get_player_name()}!")
            attack_execution(player_2, player_1)
            save_game(save, players[0], current_level)

    current_level += 1
