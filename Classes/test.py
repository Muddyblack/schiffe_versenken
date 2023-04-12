import msvcrt

while True:
    if msvcrt.kbhit():
        key = msvcrt.getch()

        # print the ASCII code of the key pressed
        print(f"Key pressed: {key}")

        if key == b"\xe0":
            arrow = msvcrt.getch()

            # print the ASCII code of the second part of the key press
            print(f"Arrow key: {arrow}")

            if arrow == b"H":
                print("Up arrow key pressed")
            elif arrow == b"P":
                print("Down arrow key pressed")
            elif arrow == b"K":
                print("Left arrow key pressed")
            elif arrow == b"M":
                print("Right arrow key pressed")
