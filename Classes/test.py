import keyboard


def get_arrow_key():
    while True:
        if keyboard.is_pressed("up"):
            while keyboard.is_pressed("up"):
                pass
            return "up"

        elif keyboard.is_pressed("down"):
            while keyboard.is_pressed("down"):
                pass
            return "down"

        elif keyboard.is_pressed("left"):
            while keyboard.is_pressed("left"):
                pass
            return "left"

        elif keyboard.is_pressed("right"):
            while keyboard.is_pressed("right"):
                pass
            return "right"

        elif keyboard.read_key() != "":
            print("Invalid direction")
            continue
        break
