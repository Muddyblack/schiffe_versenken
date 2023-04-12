from Functions import file_helper
import os
path = os.path.dirname(os.path.abspath(__file__))
print(path)

txt = file_helper.read_file(".\\Saving\\brudddi.txt")
print(txt)