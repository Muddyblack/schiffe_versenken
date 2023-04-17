import os
import subprocess

if os.name == "nt":
    import winsound
else:
    pass


def start(file):
    if os.name == "nt":
        process = winsound.PlaySound(file, winsound.SND_ASYNC)
    else:
        # Use the `aplay` command to play the WAV file if available
        try:
            aplay_cmd = ["aplay", "-q", file]
            return subprocess.Popen(aplay_cmd)
        except OSError:
            try:
                vlc_cmd = ["cvlc", "--play-and-exit", file]
                return subprocess.Popen(vlc_cmd)
            except OSError:
                try:
                    # Use the `sox` command to play the WAV file if `aplay` is not available
                    sox_cmd = ["play", "-q", file]
                    return subprocess.Popen(sox_cmd)
                except OSError:
                    print("No Module on this machine to play wav files!")


def stop(process):
    if os.name == "nt":
        winsound.PlaySound(None, winsound.SND_PURGE)
    else:
        process.kill()
