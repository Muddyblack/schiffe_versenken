import pickle
import sys
import os
import pprint
from tkinter import filedialog

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

# pylint: disable=wrong-import-position
from Library.file_helper import read_file

WORK_PATH = os.path.dirname(os.path.realpath(__file__))
SAVE_PATH = f"{WORK_PATH}/savePath.txt"

try:
    WORK_PATH = read_file(SAVE_PATH)
except FileNotFoundError:
    pass

file = filedialog.askopenfilename(
    initialdir=f"{WORK_PATH}",
    title="Select Files",
    filetypes=(
        ("all files", "*.*"),
        ("Pickel", "*.pkl, *.pickel, *.obj, *.info"),
        ("Text", "*.txt"),
        ("Json", "*.json"),
    ),
)

while True:
    what_do = input("r for read or c to convert back: ").strip().lower()

    if what_do == "r" or what_do == "c":
        break

if what_do == "r":
    # Load pickle file
    obj = pickle.load(open(file, "rb"))

    with open(f"{os.path.splitext(file)[0]}.json", "a") as f:
        pprint.pprint(obj, stream=f)

else:
    # Load text file
    with open(file, "r") as f:
        data_str = f.read()

    # Convert to Python object
    data = eval(data_str)

    # Save as pickle file
    with open(f"{os.path.splitext(file)[0]}.pkl", "wb") as f:
        pickle.dump(data, f)
