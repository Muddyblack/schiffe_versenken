import sys

if sys.platform.startswith("win"):
    if sys.maxsize > 2**32:
        import key_tracker_x64 as key_tracker
    else:
        import key_tracker_x86 as key_tracker
else:
    import key_tracker_x86_64 as key_tracker


def get_pressed_key():
    key = key_tracker.read_key()

    if sys.platform.startswith("win"):
        if key == 13:
            return "enter"
        elif key == 32:
            return "space"
        elif key == 72:
            return "up"
        elif key == 80:
            return "down"
        elif key == 77:
            return "right"
        elif key == 75:
            return "left"
        else:
            return key

    else:
        if key == 10:
            return "enter"
        elif key == 32:
            return "space"
        elif key == 27:
            key = key_tracker.read_key()
            if key == 91:
                key = key_tracker.read_key()
                if key == 65:
                    return "up"
                elif key == 66:
                    return "down"
                elif key == 67:
                    return "right"
                elif key == 68:
                    return "left"
        else:
            return key


if __name__ == "__main__":
    while True:
        key = get_pressed_key()
        if key != 0:
            print(key)
