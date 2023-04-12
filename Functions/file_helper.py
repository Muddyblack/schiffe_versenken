def read_file(file_path):
    with open(file_path, "r") as f:
        txt_lines = f.readlines()

        for r in range(len(txt_lines)):
            txt_lines[r]= txt_lines[r].replace('\n','')

    return txt_lines

# how to use : file_text_replacer(path_of_file, [stringtext], [inline_as_integer_number])
def file_line_replacer(file, change_input, line):
    
    data = read_file(file)

    for pointing,x in enumerate(change_input):
        try:
            data[line[pointing]-1] = change_input[pointing]
        except:
            data.append("")


    with open(file, 'w', encoding="utf8") as file_to_replace:
        data_len = len(data)

        for x in data:
            if data_len > 1:
                file_to_replace.writelines(f"{x}\n")
            else:
                file_to_replace.writelines(f"{x}")
            
            data_len-=1
