"""
- Handles game-logic, game-saving and loading
- Manages players and their game-fields. 
"""
import os
import time
import pickle
import gc
import random
import simpleaudio
import keyboard

from Library import console_helper
from Library.keyboard_helper import clear_input

from Classes.player import Player
from Classes.game_field import GameField


class Game:
    """
    The Game class serves as the main entry point for running the game
    """

    def __init__(self, project_path):
        os.system(f"{console_helper.RESET}")
        # Paths
        self.__game_data_path = f"{project_path}/GameData"
        self.__save_games_path = f"{self.__game_data_path}/saves"
        self.__sound_path = f"{self.__game_data_path}/sound"
        os.makedirs(self.__save_games_path, exist_ok=True)

        self.__players = None
        self.__save_name = None
        self.__current_level = None

        self.start_up()

        self.__last_turn_player = self.__players[0]

    # getter
    def get_players(self):
        """Returns an Array of the players"""
        return self.__players

    def get_save_path(self):
        """Returns the Absolete save Path of the current Game"""
        return f"{self.__save_games_path}/{self.__save_name}"

    def get_sound_path(self):
        """Returns the path of the sound_folder"""
        return f"{self.__sound_path}"

    def get_current_level(self):
        """Returns the current level of the game"""
        return self.__current_level

    def get_last_turn_player(self):
        """Returns th players who has the tun"""
        return self.__last_turn_player

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

    def __ask_name(self, question):
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
                msg = f"The name is too short it has: {len(name)} min length: {min_name_len}"
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

        save_dir = f"{self.__save_games_path}/{self.__save_name}"
        os.makedirs(save_dir, exist_ok=True)

        with open(f"{save_dir}/players.obj", "wb") as obj:
            pickle.dump(player_list, obj)
        with open(f"{save_dir}/game.info", "wb") as obj:
            pickle.dump(game_info, obj)

    def load_game(self):
        """
        Loads a saved game.

        Returns:
            -(tuple): two GameField instances and dictionary with game-infos
        """
        with open(
            f"{self.__save_games_path}/{self.__save_name}/players.obj", "rb"
        ) as playerpickle:
            player_list = pickle.load(playerpickle)
        with open(
            f"{self.__save_games_path}/{self.__save_name}/game.info", "rb"
        ) as playerpickle:
            game_info = pickle.load(playerpickle)

        self.__last_turn_player = game_info["last_turn_player"]
        self.__current_level = game_info["level"]

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

        if self.__last_turn_player == f_1.owner.get_player_name():
            fields = (f_1, f_2)
        elif self.__last_turn_player == f_2.owner.get_player_name():
            fields = (f_2, f_1)
        else:
            # Coin flipping who will start the Game
            starter = random.randint(0, 1)
            if starter == 0:
                fields = (f_1, f_2)
            else:
                fields = (f_2, f_1)

        self.__players = fields

    def __create__new_game(self, existing_saves):
        """
        Creates a new game.

        Returns:
            - (tuple): two GameField instances and dictionary with game-infos
        """
        while True:
            print("Hello you decided to create a new Save-game")
            save_name = f'{self.__ask_name("Enter the save name you wish to use: ").replace(" ", "_")}_save'

            if save_name in existing_saves:
                print("This name does already exist!")
            else:
                self.__save_name = save_name
                break

        opponent = ""

        p1_name = self.__ask_name("Nice, so what is your name: ")
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
                p2_name = self.__ask_name(
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

        self.__players = fields
        self.__current_level = 0

    def __start_screen(self):
        """Prints a beautiful ASCII-Logo for the game to the console"""
        sound_process = simpleaudio.WaveObject.from_wave_file(
            f"{self.__sound_path}/Start-Screen.wav"
        ).play()

        start_screen_animation_path = f"{self.__game_data_path}/start_screen_animation"

        files = [
            os.path.abspath(os.path.join(start_screen_animation_path, file))
            for file in os.listdir(start_screen_animation_path)
        ]
        frames = sorted(files)

        stop = False
        while not stop:
            if not sound_process.is_playing():
                sound_process = simpleaudio.WaveObject.from_wave_file(
                    f"{self.__sound_path}/Start-Screen.wav"
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
            f"{self.__sound_path}/Start_game.wav"
        ).play()

        clear_input()
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
        Allows the user to select a saved game from a list of saved game directories displayed on the console.
        The user uses arrow-keys and the enter-key

        Returns:
            - (str): The selected game directory.
        """
        selected_save_game_index = 0
        save_games_len = len(exist_save_games)

        print("Use up and down arrows to navigate\nUse Spacebar to sleect the game")
        self.__display_save_games(exist_save_games, selected_save_game_index)

        while True:
            # Handle arrow key presses to move the selected save game index up or down

            if keyboard.is_pressed("up") and selected_save_game_index > 0:
                sound_process = simpleaudio.WaveObject.from_wave_file(
                    f"{self.__sound_path}/Menu-Select.wav"
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
                    f"{self.__sound_path}/Menu-Select.wav"
                ).play()

                selected_save_game_index += 1
                console_helper.refresh_console_lines(save_games_len)
                self.__display_save_games(exist_save_games, selected_save_game_index)
                while keyboard.is_pressed("down"):
                    pass
                sound_process.wait_done()

            elif keyboard.is_pressed(" "):
                break

        self.__save_name = exist_save_games[selected_save_game_index]
        print(f"Selected save game: {os.path.basename(self.__save_name)}\n")
        simpleaudio.WaveObject.from_wave_file(
            f"{self.__sound_path}/Selected.wav"
        ).play()

    def start_up(self):
        """
        Sets up the initial game environment
        If the user chooses to load an old save, it loads the save game and returns the GameField instances for both players.
        Otherwise, it asks for the player's name, whether they want to play against a real person or a bot, and starts the game
        by randomly choosing which player goes first.

        Returns:
            A dictionary with keys "players" and "save_name". The value for the key "players" is a list of two GameField instances
            representing the players. The value for the key "save_name" is a string representing the name of the save game.
        """
        self.__start_screen()
        exist_save_games = [
            f.name
            for f in os.scandir(self.__save_games_path)
            if f.is_dir() and not f.is_file() and f.name.endswith("_save")
        ]

        load = ""
        if len(exist_save_games) == 0:
            load = "n"

        while load not in ("y", "n"):
            load = input("Do you want to load an old save? [y/n]: ").lower().strip()
            clear_input()

        if load == "y":
            self.__select_savegame(exist_save_games)
            return self.load_game()

        return self.__create__new_game(exist_save_games)
