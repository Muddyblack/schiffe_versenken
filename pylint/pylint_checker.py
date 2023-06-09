"""Allows you to select a file via Explorer to get the pylint results fast."""
import sys
import os
from tkinter import filedialog
import subprocess

os.environ[
    "PYTHONPATH"
] = f"{os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))}"

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
)

# Pylint mus be deactivated because we have to append the project path directory here.
# Python cannot go upper than the runnings script directory
# pylint: disable=wrong-import-position
from library import file_helper


WORK_PATH = os.path.dirname(os.path.realpath(__file__))
SAVE_PATH = f"{WORK_PATH}/savePath.txt"

try:
    WORK_PATH = file_helper.read_file(SAVE_PATH)
except FileNotFoundError:
    pass

FILEPATHS = filedialog.askopenfilenames(
    initialdir=f"{WORK_PATH}",
    title="Select Files",
    filetypes=(("Python files", "*.py"), ("all files", "*.*")),
)

with open(SAVE_PATH, "w", encoding="utf8") as f:
    try:
        f.write(f"{FILEPATHS [0]}")
    except IndexError:
        pass

for file in FILEPATHS:
    try:
        with subprocess.Popen(
            [
                "pylint",
                file,
                "--output-format=colorized",
            ],
            stdin=subprocess.PIPE,
        ) as process:
            pass

    except subprocess.CalledProcessError as e:
        print(f"Error processing file '{file}': {e}")

input("Hit any key to continue...")
