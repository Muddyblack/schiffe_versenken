"""
This allows to play wav files on windows AND most Linux machines (aplay is on pretty every Linux system)
cvlc works only as non root user because it ist still trying to get acces to the CD-Drive. (Security)
"""
import os
import subprocess
import time

if os.name == "nt":
    import winsound


def play(file):
    """
    Starts playing the given file
    """
    if os.name == "nt":
        process = winsound.PlaySound(file, winsound.SND_ASYNC)
    else:
        players = ["aplay", "cvlc", "play"]
        for player in players:
            try:
                cmd = [player, "-q", file]
                with subprocess.Popen(subprocess.Popen(cmd)) as process:
                    pass
            except OSError:
                pass

        print("No Module on this machine to play wav files!")
    return process


def stop(process):
    """
    stops the given process of a playing file.
    """
    if os.name == "nt":
        winsound.PlaySound(None, winsound.SND_PURGE)
    else:
        try:
            process.kill()
        except OSError:
            print("Couldn't kill the audio-player")


if __name__ == "__main__":
    # an example
    sound = play(
        "/home/muddyblack/Downloads/Schiffe_Versenken_KEYBOARD_INPUT_CUSTOM_SAVE/GameData/sound/Start-Screen.wav"
    )
    time.sleep(10)
    stop(sound)
