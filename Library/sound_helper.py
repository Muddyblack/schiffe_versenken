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
        process = subprocess.Popen(['paplay', file], stdin=subprocess.PIPE)
    return process

def stop(process):
    if os.name == "nt":
        winsound.PlaySound(None, winsound.SND_PURGE)
    else:
        process.kill()
