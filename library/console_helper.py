"""Contains functions that help using the terminal as I/O"""
import os
import sys

# Define color codes for ANSI escape sequences
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
MAGENTA = "\033[35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
RESET = "\033[0m"


def max_line_length(lines):
    """Compute the maximum length of lines in a list."""
    max_length = 0
    for line in lines:
        line_length = len(line)
        if line_length > max_length:
            max_length = line_length
    return max_length


def clear_console():
    """clearing the console"""
    os.system("cls" if os.name == "nt" else "clear")


def refresh_console_lines(lines):
    """Clears the specified number of lines from the console output."""
    for i in range(lines):
        sys.stdout.write("\033[F")  # Move the cursor up one line
        sys.stdout.write("\033[K")  # Clear line


def print_side_by_side(strings, padding=4, strip=False):
    """
    Prints n strings side by side in the console with padding between them (ALLOWS ANSI)
    """
    strings_lines = [s.splitlines() for s in strings]
    max_lines = max_line_length(strings_lines)

    # Loop through each line and print them side by side
    for i in range(max_lines):
        for j, lines in enumerate(strings_lines):
            if i < len(lines):
                # Strip line if wanted
                if strip:
                    line = lines[i].strip()
                else:
                    line = lines[i]
                print(line.ljust(len(line) + padding), end="")

                # Adding padding
                if j < len(strings_lines) - 1:
                    print(" " * padding, end="")
            else:
                print(" " * (len(lines[0]) + padding), end="")
        print()
