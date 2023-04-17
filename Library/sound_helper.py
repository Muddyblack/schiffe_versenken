import os
import subprocess

if os.name == "nt":
    import winsound

def start(file):
    if os.name == "nt":
        process = winsound.PlaySound(file, winsound.SND_ASYNC)
    else:
        # Use the `aplay` command to play the WAV file if available
        try:
            vlc_cmd = ["cvlc", "-q", file]
            process = subprocess.Popen(vlc_cmd)
        except OSError:
            try:
                aplay_cmd = ["aplay", "-q", file]
                process = subprocess.Popen(aplay_cmd)
            except OSError:
                try:
                    sox_cmd = ["play", "-q", file]
                    process = subprocess.Popen(sox_cmd)
                except OSError:
                    print("No Module on this machine to play wav files!")
    return process

def stop(process):
    if os.name == "nt":
        winsound.PlaySound(None, winsound.SND_PURGE)
    else:
        try:
            process.kill()
        except OSError:
            pass