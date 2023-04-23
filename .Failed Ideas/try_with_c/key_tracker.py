# pylint: disable=C)
"""
This is the start of a module for python using C to get Keyboard events without blocking the main script.
It would not require root access on Linux like the already existing keyboard-module does!
"""

####
#
# THIS IS NOT FINISHED AND IN DEV
#
###
import sys
import os

# Import the for different system and Python versions compiled Code
# At the moment only Python 3.11.2 for Windows and Linux(Debian11)
if os.name == "nt":
    if sys.maxsize > 2**32:
        import key_tracker_x64 as key_tracker
    else:
        import key_tracker_x86 as key_tracker
else:
    import key_tracker_x86_64 as key_tracker

if os.name == "nt":

    def get_pressed_key():
        """
        STILL in DEV
        Was used for another script to get some keys as text form
        IN FUTURE: This Moethod will be renamed to return for all Keys their String-Names
        """
        key = key_tracker.read_key()
        keyname = ""
        if key == 13:
            keyname = "enter"
        elif key == 32:
            keyname = "space"
        elif key == 72:
            keyname = "up"
        elif key == 80:
            keyname = "down"
        elif key == 77:
            keyname = "right"
        elif key == 75:
            keyname = "left"
        else:
            keyname = key
        return keyname

else:

    def get_pressed_key():
        """
        STILL in DEV
        Was used for another script to get some keys as text form
        IN FUTURE: This Moethod will be renamed to return for all Keys their String-Names
        """
        key = key_tracker.read_key()
        if key == 10:
            keyname = "enter"
        elif key == 32:
            keyname = "space"
        elif key == 27:
            key = key_tracker.read_key()
            if key == 91:
                key = key_tracker.read_key()
                if key == 65:
                    keyname = "up"
                elif key == 66:
                    keyname = "down"
                elif key == 67:
                    keyname = "right"
                elif key == 68:
                    keyname = "left"
        else:
            keyname = key
        return keyname


if __name__ == "__main__":
    while True:
        pressed_key = get_pressed_key()
        if pressed_key != 0:
            print(pressed_key)
