"""
This module provides a function for detecting which arrow key is pressed on the keyboard.
"""
import keyboard


def get_arrow_key():
    """
    Detects which arrow key is pressed on the keyboard and returns the corresponding direction.

    Returns:
        str: The direction of the arrow key that is pressed on the keyboard. It can be one of the following:
             "up", "down", "left", or "right".
    """

    while True:
        if keyboard.is_pressed("up"):
            return "up"

        if keyboard.is_pressed("down"):
            return "down"

        if keyboard.is_pressed("left"):
            return "left"

        if keyboard.is_pressed("right"):
            return "right"
