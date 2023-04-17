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

    # getter
    def get_bot(self):
        """Returns the bot instance."""
        return self.__bot

    def get_player_name(self):
        """Returns the player's name."""
        return self.__player_name

    # setter
    def set_bot(self):
        """Sets the bot instance."""
        return self.__bot

    def set_player_name(self):
        """Sets the player's name."""
        return self.__player_name
