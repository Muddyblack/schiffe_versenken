from Functions import file_helper
import os
path = f"{os.path.dirname(os.path.abspath(__file__))}"
print(path)

txt = file_helper.read_file(f"{path}/Saving/brudddi.txt")
print(txt)
