def read_file(file_path):
    with open(file_path, "r", encoding="utf8") as file:
        txt_lines = file.readlines()

        for elem in enumerate(txt_lines):
            txt_lines[elem[0]] = txt_lines[elem[0]].replace("\n", "")

    return txt_lines


# how to use : file_text_replacer(path_of_file, [stringtext], [inline_as_integer_number])
def file_line_replacer(file, change_input, line):
    data = read_file(file)

    for pointing in enumerate(change_input):
        try:
            data[line[pointing[0]] - 1] = change_input[pointing[0]]
        except:
            data.append("")

    with open(file, "w", encoding="utf8") as file_to_replace:
        data_len = len(data)

        for elem in data:
            if data_len > 1:
                file_to_replace.writelines(f"{elem}\n")
            else:
                file_to_replace.writelines(f"{elem}")

            data_len -= 1
