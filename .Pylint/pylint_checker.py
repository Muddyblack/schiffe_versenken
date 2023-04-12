"""This Allows you to select a file to get the pylint results fast"""

import sys
import os
from tkinter import filedialog
import pylint

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
from Library.file_helper import read_file

work_path = os.path.dirname(os.path.realpath(__file__))
save_path = f"{work_path}\\savePath.txt"

try:
    work_path = read_file(save_path)
except FileNotFoundError:
    pass

filepaths = filedialog.askopenfilenames(
    initialdir=f"{work_path}",
    title="Select Files",
    filetypes=(("Python files", "*.py"), ("all files", "*.*")),
)

with open(save_path, "w", encoding="utf8") as f:
    try:
        f.write(f"{filepaths[0]}")
    except IndexError:
        pass

for file in filepaths:
    pylint.run_pylint(
        argv=[file, "--output-format=colorized", "--max-line-length=160"]
    )  # after first one it just kills the program...
