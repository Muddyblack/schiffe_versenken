import os
import subprocess
import time

if os.name == "nt":
    import winsound


def start(file):
    if os.name == "nt":
        process = winsound.PlaySound(file, winsound.SND_ASYNC)
    else:
        players = ["aplay", "cvlc", "play"]
        for player in players:
            try:
                cmd = [player, "-q", file]
                process = subprocess.Popen(cmd)
                return process
            except OSError:
                pass

        print("No Module on this machine to play wav files!")


def stop(process):
    if os.name == "nt":
        winsound.PlaySound(None, winsound.SND_PURGE)
    else:
        try:
            process.kill()
        except OSError:
            print("Couldn't kill the audio-player")




if  __name__ == "__main__":
    sound = start("/home/muddyblack/Downloads/Schiffe_Versenken_KEYBOARD_INPUT_CUSTOM_SAVE/GameData/sound/Start-Screen.wav")
    time.sleep(10)
    stop(sound)