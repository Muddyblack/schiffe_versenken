"""Player Module"""
import json
from library import game_paths
from library import console_helper

class Player:
    """
    The Player class represents the user with its name or if it is a bot and his ships.
    It has several methods to set and get the user attributes.
    """

    def __init__(self, bot=False, name="bot"):
        self.__bot = bot

        self.__player_name = name

        self.__botcache = []

        self.__ship_preferences = {}
        self.load_ship_preferences()

        self.__ships = self.init_ships()

    # getter
    def get_bot(self):
        """Returns the bot instance."""
        return self.__bot

    def get_player_name(self):
        """Returns the player's name."""
        return self.__player_name

    def get_ships(self):
        """Returns the ship's dictionary."""
        return self.__ships

    def get_ship_amount(self):
        """Returns the amount of ships the player currently has"""
        index = 0
        for key in self.__ships:
            index += len(self.__ships[key])

        return index

    def get_botcache(self):
        """Returns the cache of already attacked Positions"""
        return self.__botcache

    def get_ship_preferences(self):
        """Returns the dictionary with all allowed ships and their settings"""
        return self.__ship_preferences

    # init
    def init_ships(self):
        """Returning the starter ships Dictionary"""
        return {key: [] for key in self.__ship_preferences.keys()}

    # setter
    def set_bot(self, value):
        """Sets the bot instance."""
        if not isinstance(value, bool):
            raise ValueError("Only accepts boolean")
        self.__bot = value

    def set_player_name(self, name):
        """Sets the player's name."""
        self.__player_name = name

    def set_ships(self, value):
        """Sets the ship's dictionary."""
        self.__ships = value

    def ships_after_attack(self, target_cell):
        """Removes hitted cells from ships and checks if there is still something left to play"""
        breaking = False
        for key in self.__ships:
            for ship_ind, ship in enumerate(self.__ships[key]):
                if target_cell in ship:
                    self.__ships[key][ship_ind].remove(target_cell)
                    if len(self.__ships[key][ship_ind]) == 0:
                        self.__ships[key] = [x for x in self.__ships[key] if x != []]
                        print(f"{console_helper.RED}{key} got Destroyed{console_helper.RESET}")
                else:
                    continue
                breaking = True
                break
            if breaking:
                break

    def add_ship(self, element, pos):
        """Sets the ship's dictionary."""
        self.__ships[element].append(pos)

    def set_botcache(self, cache):
        """Sets the cache of already attacked Positions"""
        self.__botcache = cache

    def load_ship_preferences(self):
        """Adding ships with their settings of length, max-amount, etc from json file"""
        with open(
            f"{game_paths.GAME_DATA_PATH}/ships.json", "r", encoding="utf-8"
        ) as file:
            self.__ship_preferences = json.load(file)
