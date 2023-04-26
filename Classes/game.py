"""
- Handles game-logic, game-saving and loading
- Manages players and their game-fields. 
"""
import os
import time
import random
import pickle
import gc
import simpleaudio
import keyboard

from Library import console_helper
from Library import keyboard_helper
from Library import game_paths

from Classes.player import Player
from Classes.game_field import GameField


class Game:
    """
    The Game class serves as the main entry point for running the game
    """

    def __init__(self):
        os.system(f"{console_helper.RESET}")
        os.makedirs(game_paths.SAVE_GAMES_PATH, exist_ok=True)

        self.__players = None
        self.__save_name = None
        self.__current_level = None

        self.start_up()
        self.__last_turn_player = self.__players[0]
        time.sleep(0.3)

    # getter
    def get_save_path(self):
        """Returns the Absolete save Path of the current Game"""
        return f"{game_paths.SAVE_GAMES_PATH}/{self.__save_name}"

    def get_players(self):
        """Returns an Array of the players"""
        return self.__players

    def get_current_level(self):
        """Returns the current level of the game"""
        return self.__current_level

    def get_last_turn_player(self):
        """Returns th players who has the tun"""
        return self.__last_turn_player

    def get_if_botgame(self):
        """Returns True if only bots will play against each other"""

        for player in self.__players:
            if not player.owner.get_bot():
                return False
        return True

    # setter
    def set_players(self, players):
        """Sets the players Variable of the class Game"""
        self.__players = players

    def set_current_level(self, level):
        """Sets the current level of the game"""
        self.__current_level = level

    def set_last_turn_player(self, player):
        """Returns th players who has the tun"""
        self.__last_turn_player = player

    # Class functions

    def __ask_name(self, question, duplication=""):
        """
        Asks the user to enter his name and checks:
            - if it is not empty or longer than 15 characters
            - contains not allowed characters
            - is duplicated
        """
        not_allowed_chars = r'\/:*?"<>|'
        min_name_len = 3
        max_name_len = 15

        while True:
            keyboard_helper.clear_input()
            name = input(f"\n{question}").strip()

            if name == "":
                msg = "This is just an empty String!"
            elif len(name) > max_name_len:
                msg = f"The name is too long it has: {len(name)} character allowed: {max_name_len}"
            elif len(name) < min_name_len:
                msg = f"The name is too short it has: {len(name)} min length: {min_name_len}"
            elif any(char in name for char in not_allowed_chars):
                msg = f"{not_allowed_chars} are not allowed in your name!"
            elif name in duplication:
                msg = f"{name} is already taken. Choose another name!"
            else:
                break

            print(msg)

        return name

    def save_game(self):
        """Saves the current state of the game in a binary file format."""
        player_list = []
        game_info = {
            "last_turn_player": self.__last_turn_player.owner.get_player_name(),
            "level": self.__current_level,
        }

        # collecting data from all instances of GameField class
        for obj in gc.get_objects():
            if isinstance(obj, GameField):
                player_info = {
                    "name": obj.owner.get_player_name(),
                    "bot": obj.owner.get_bot(),
                    "botcache": obj.owner.get_botcache(),
                    "ships": obj.owner.get_ships(),
                    "boatfield": obj.get_boatfield(),
                    "hitfield": obj.get_hitfield(),
                }
                player_list.append(player_info)

        # Write to file and create path if not existing
        save_dir = f"{game_paths.SAVE_GAMES_PATH}/{self.__save_name}"
        os.makedirs(save_dir, exist_ok=True)
        with open(f"{save_dir}/players.obj", "wb") as file:
            pickle.dump(player_list, file)
        with open(f"{save_dir}/game.info", "wb") as file:
            pickle.dump(game_info, file)

    def load_game(self):
        """
        Loads a saved game.
        """

        # Reading required files
        with open(
            f"{game_paths.SAVE_GAMES_PATH}/{self.__save_name}/players.obj", "rb"
        ) as playerpickle:
            player_list = pickle.load(playerpickle)
        with open(
            f"{game_paths.SAVE_GAMES_PATH}/{self.__save_name}/game.info", "rb"
        ) as playerpickle:
            game_info = pickle.load(playerpickle)

        self.__last_turn_player = game_info["last_turn_player"]
        self.__current_level = game_info["level"]
        field_list = []

        # creating objects from save-file
        for obj in player_list:
            player = Player(name=obj["name"], bot=obj["bot"])
            player.set_ships(obj["ships"])
            player.set_botcache(obj["botcache"])
            field = GameField(player)
            field.set_boatfield(obj["boatfield"])
            field.set_hitfield(obj["hitfield"])

            field_list.append(field)

        def rotate_array_backwards(arr):
            first_element = arr[0]
            # Postpone elements one to the left
            for i in range(0, len(arr) - 1):
                arr[i] = arr[i + 1]
            # set last elem to the first elem
            arr[-1] = first_element
            return arr

        # Checking who had last turn
        check_ind = 0
        while True:
            if check_ind >= len(field_list):
                # if no existing starter, probability calculation gonna set one
                first_cache = field_list[0]
                random_starter = random.randint(0, len(field_list) - 1)
                field_list[0] = field_list[random_starter]
                field_list[random_starter] = first_cache
                break
            if field_list[0].owner.get_player_name() != self.__last_turn_player:
                field_list = rotate_array_backwards(field_list)
            else:
                break
            check_ind += 1

        self.__players = field_list

    def __yes_no_question(self, question):
        """
        Function that returns True or Flase for yes or no questions
        """
        while True:
            user_input = input(f"{question} [y/n] ").lower().strip()
            if user_input in ("y", "yes", ""):
                return True
            if user_input in ("n", "no"):
                return False

            print("You can only answer with yes or no!")

    def __create__new_game(self, existing_saves, player_num=2):
        """
        Creates a new game.
        """

        # Asks for the save-game name
        print("Hello you decided to create a new Save-game")
        existing_saves_names = [elem.replace("_save", "") for elem in existing_saves]
        self.__save_name = f'{self.__ask_name("Enter the save name you wish to use: ", existing_saves_names).replace(" ", "_")}_save'

        # Asks if the User should be a bot, ask for the name and create the GamField
        field_list = []
        player_names = []
        bots = 0

        for index in range(player_num):
            player_name = ""
            is_bot = False

            if self.__yes_no_question(f"Welcome Player{index+1}!\nAre You a bot?"):
                bots += 1
                is_bot = True
                player_name = f"bot_{bots}"
            else:
                player_name = self.__ask_name(
                    "Nice, so what is your name: ", player_names
                )
            player_names.append(player_name)
            field_list.append(GameField(Player(bot=is_bot, name=player_name)))

        # Random gonna decide who starts
        first_cache = field_list[0]
        random_starter = random.randint(0, len(field_list) - 1)
        field_list[0] = field_list[random_starter]
        field_list[random_starter] = first_cache

        # Finish and set Variables
        self.__players = field_list
        self.__current_level = 0

    def __start_screen(self):
        """Prints a beautiful ASCII-Logo for the game to the console"""
        sound_process = simpleaudio.WaveObject.from_wave_file(
            f"{game_paths.SOUND_PATH}/Start-Screen.wav"
        ).play()

        start_screen_animation_path = (
            f"{game_paths.GAME_DATA_PATH}/start_screen_animation"
        )

        # Get all files for animation and print them in loop until interrupted by user.
        files = [
            os.path.abspath(os.path.join(start_screen_animation_path, file))
            for file in os.listdir(start_screen_animation_path)
        ]
        frames = sorted(files)

        stop = False
        while not stop:
            if not sound_process.is_playing():
                sound_process = simpleaudio.WaveObject.from_wave_file(
                    f"{game_paths.SOUND_PATH}/Start-Screen.wav"
                ).play()

            for frame in frames:
                with open(frame, "r", encoding="utf-8") as file:
                    string = (
                        file.read()
                        .replace("{BROWN}", console_helper.BROWN)
                        .replace("{LIGHT_GRAY}", console_helper.LIGHT_GRAY)
                        .replace("{MAGENTA}", console_helper.MAGENTA)
                        .replace("{RESET}", console_helper.RESET)
                    )

                print(string)

                print(
                    f"\n{console_helper.LIGHT_BLUE}Hit the Enter Key, to continue{console_helper.RESET}",
                    end="",
                )

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

                console_helper.clear_console()

        time.sleep(0.1)
        sound_process.stop()
        simpleaudio.WaveObject.from_wave_file(
            f"{game_paths.SOUND_PATH}/Start_game.wav"
        ).play()

        keyboard_helper.clear_input()
        console_helper.clear_console()

    def __display_save_games(self, save_games, selected_save_game_index):
        """Displays the list of save games with the currently selected save game highlighted"""

        for i in enumerate(save_games):
            game_name = os.path.basename(save_games[i[0]])
            if i[0] == selected_save_game_index:
                print(f"{console_helper.CYAN}> {game_name}{console_helper.RESET}")
            else:
                print(f"  {game_name}")

    def __select_savegame(self, exist_save_games):
        """
        - Allows the user to select a saved game from a list of saved game directories displayed on the console.
        - The user uses arrow-keys and the space-key
        """
        selected_save_game_index = 0
        save_games_len = len(exist_save_games)
        print("Use up and down arrows to navigate\nUse Spacebar to sleect the game")

        self.__display_save_games(exist_save_games, selected_save_game_index)

        while True:
            # Handle arrow key presses to move the selected save game index up or down

            if keyboard.is_pressed("up") and selected_save_game_index > 0:
                sound_process = simpleaudio.WaveObject.from_wave_file(
                    f"{game_paths.SOUND_PATH}/Menu-Select.wav"
                ).play()

                selected_save_game_index -= 1
                console_helper.refresh_console_lines(save_games_len)
                self.__display_save_games(exist_save_games, selected_save_game_index)

                while keyboard.is_pressed("up"):
                    pass
                sound_process.wait_done()

            elif (
                keyboard.is_pressed("down")
                and selected_save_game_index < len(exist_save_games) - 1
            ):
                sound_process = simpleaudio.WaveObject.from_wave_file(
                    f"{game_paths.SOUND_PATH}/Menu-Select.wav"
                ).play()

                selected_save_game_index += 1
                console_helper.refresh_console_lines(save_games_len)
                self.__display_save_games(exist_save_games, selected_save_game_index)
                while keyboard.is_pressed("down"):
                    pass
                sound_process.wait_done()

            elif keyboard.is_pressed(" "):
                break

        # Set Variable and exit function with playing start-sound
        self.__save_name = exist_save_games[selected_save_game_index]
        print(f"Selected save game: {os.path.basename(self.__save_name)}\n")

        simpleaudio.WaveObject.from_wave_file(
            f"{game_paths.SOUND_PATH}/Selected.wav"
        ).play()

    def start_up(self):
        """
        Sets up the initial game environment.
        If the user chooses to load an old save, it loads the save game and returns the GameField instances for all players.
        Otherwise, it asks for the player's name, whether they want to play against a real person or a bot, and starts the game
        by randomly choosing which player goes first.

        Returns:
            - A dictionary with keys "players" and "save_name".
                - The value for the key "players" is a list of GameField instances representing the players.
                - The value for the key "save_name" is a string representing the name of the save game.
        """
        self.__start_screen()
        exist_save_games = [
            f.name
            for f in os.scandir(game_paths.SAVE_GAMES_PATH)
            if f.is_dir() and not f.is_file() and f.name.endswith("_save")
        ]

        if len(exist_save_games) != 0:
            if self.__yes_no_question("Do you want to load an old save?"):
                self.__select_savegame(exist_save_games)
                return self.load_game()

        return self.__create__new_game(exist_save_games)
