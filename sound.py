import os
import time
from Library import sound_helper

# Open the WAV file
file_path = f"{os.path.join(os.path.dirname(os.path.realpath(__file__)))}/GameData/sound/Start-Screen.wav"

sound_helper.start(file_path)
time.sleep(300)
sound_helper.stop(file_path)
