import curses

# initialize curses
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
    while True:
        # get user input
        char = screen.getch()

        # process input
        if char == curses.KEY_UP:
            print("Up arrow key pressed")
        elif char == curses.KEY_DOWN:
            print("Down arrow key pressed")
        elif char == curses.KEY_LEFT:
            print("Left arrow key pressed")
        elif char == curses.KEY_RIGHT:
            print("Right arrow key pressed")
        elif char == ord('q'):
            break

finally:
    # clean up curses
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()