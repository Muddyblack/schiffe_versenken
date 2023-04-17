import os
import subprocess

if os.name == "nt":
    import winsound


def start(file):
    if os.name == "nt":
        process = winsound.PlaySound(file, winsound.SND_ASYNC)
    else:
        players = ["aplay, cvlc, play"]
        for player in players:
            cmd = vlc_cmd = [player, "-q", file]
            process = subprocess.Popen(cmd)
            return process
            try:
                aplay_cmd = ["aplay", "-q", file]
                return subprocess.Popen(aplay_cmd)
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
