""" Functions helping reading and replacing text from and in files """


def read_file(file_path):
    """
    Read content of a file and return it as a list of lines (newline characters removed)

    Args:
        file_path (str): Path to the file to read.

    Returns:
        list: A list of strings, with each string representing a line of the file (newline characters removed)
    """
    with open(file_path, "r", encoding="utf8") as file:
        txt_lines = file.readlines()

        for elem in enumerate(txt_lines):
            txt_lines[elem[0]] = txt_lines[elem[0]].replace("\n", "")

    return txt_lines


def file_line_replacer(file, change_input, line):
    """
    Replace specified lines in a file with a given replacement text.

    Args:
        file (str): The path to the file to modify.
        change_input (list): A list of strings representing the replacement text to use.
        line (list): A list of integers representing the line numbers to replace with the corresponding string in change_input.
    """
    data = read_file(file)

    for pointing in enumerate(change_input):
        try:
            data[line[pointing[0]] - 1] = change_input[pointing[0]]
        except (IndentationError, IndexError, InterruptedError):
            data.append("")

    with open(file, "w", encoding="utf8") as file_to_replace:
        data_len = len(data)

        for elem in data:
            if data_len > 1:
                file_to_replace.writelines(f"{elem}\n")
            else:
                file_to_replace.writelines(f"{elem}")

            data_len -= 1
