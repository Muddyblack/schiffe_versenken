import keyboard


def get_arrow_key():
    while True:
        if keyboard.is_pressed("up"):
            return "up"

        elif keyboard.is_pressed("down"):
            return "down"

        elif keyboard.is_pressed("left"):
            return "left"

        elif keyboard.is_pressed("right"):
            return "right"
