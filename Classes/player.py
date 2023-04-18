"""Player Module"""


class Player:
    """
    The Player class represents the user with its name or if it is a bot.
    It has several methods to set and get the user attributes.
    """

    def __init__(self, bot=False, name="Player"):
        self.__bot = bot

        if self.__bot is True:
            self.__player_name = "bot"
        else:
            self.__player_name = name

        self.__ships = {"battleship": [], "cruiser": [], "destroyer": [], "uboat": []}

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
            print(key)
            index += len(self.__ships[key])

        return index

    # setter
    def set_bot(self, value):
        """Sets the bot instance."""
        self.__bot = value

    def set_player_name(self, name):
        """Sets the player's name."""
        self.__player_name = name

    def set_ships(self, value):
        """Sets the ship's dictionary."""
        self.__ships = value

    def ships_after_attack(self, target_cell):
        """Removes hitted cells from ships and checks if there is still something left to play"""
        for key in self.__ships:
            for ship in key:
                if len(ship) == 0:
                    print("SHip Destroyed")
                    key.remove(ship)
                elif target_cell in ship:
                    ship.remove(target_cell)
                else:
                    continue
                breaking = True
                break
            if breaking:
                break

        if self.get_ship_amount() is True:
            return True

        return False

    def add_ship(self, element, pos):
        """Sets the ship's dictionary."""
        self.__ships[element].append(pos)