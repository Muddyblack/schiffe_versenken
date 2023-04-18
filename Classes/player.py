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
            index += len(self.__ships[key])

        return index

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
                        print(f"{key} got Destroyed")
                else:
                    continue
                breaking = True
                break
            if breaking:
                break

    def add_ship(self, element, pos):
        """Sets the ship's dictionary."""
        self.__ships[element].append(pos)


"""
if __name__ == "__main__":
    player = Player(name="Petra", bot=False)
    ships = {
        "battleship": [[(0, 0), (0, 1)], [(10, 0), (10, 1)]],
        "cruiser": [[(1, 1)]],
        "destroyer": [[(2, 2)]],
        "uboat": [[(3, 3)]],
    }
    shipsb = {
        "battleship": [[(1, 1)]],
        "cruiser": [[(0, 0)]],
        "destroyer": [],
        "uboat": [],
    }
    player.set_ships(shipsb)
    player.ships_after_attack((1, 1))
    player.ships_after_attack((0, 0))

    print(player.get_ships())
"""
