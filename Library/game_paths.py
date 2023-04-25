"""
Containing all main directory paths for the game
"""

import os

PROJECT_PATH = f"{os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))}"
GAME_DATA_PATH = f"{PROJECT_PATH}/GameData"
SAVE_GAMES_PATH = f"{GAME_DATA_PATH}/saves"
SOUND_PATH = f"{GAME_DATA_PATH}/sound"
