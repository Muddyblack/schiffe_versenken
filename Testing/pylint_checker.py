"""This Allows you to select a file to get the pylint results fast"""

import os
from tkinter import filedialog
import pylint

work_path = os.getcwd()

filepaths = filedialog.askopenfilenames(
    initialdir=f"{work_path}",
    title="Select Files",
    filetypes=(("Python files", "*.py"), ("all files", "*.*")),
)

for file in filepaths:
    pylint.run_pylint(argv=[file])
