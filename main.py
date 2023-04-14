import os
from Classes import game_field

project_path = f"{os.path.dirname(os.path.abspath(__file__))}"


def clear_previous_console_output():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    s1 = game_field.GameField(False)

    s2 = game_field.GameField()
    s2.set_ship(5)
    s2.show_boatfield()

    while True:
        s1.attack_enemy(s2)
        s1.show_hitfield()
        s2.show_boatfield()

