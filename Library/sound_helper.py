import time
import os

if os.name == "nt":
    import winsound


def start(file):
    if os.name == "nt":
        winsound.PlaySound(file, winsound.SND_ASYNC)
    else:
        pass


def stop(file):
    if os.name == "nt":
        winsound.PlaySound(None, winsound.SND_PURGE)
    else:
        pass
