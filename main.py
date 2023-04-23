"""This is the main module where the entire game logic gets merged"""
import os
import sys
import shutil
import random
import simpleaudio
from Library import console_helper
from Library.keyboard_helper import clear_input

from Classes.game import Game

# enables ansi escape characters in terminal
os.system(f"{console_helper.RESET}")
PROJECT_PATH = f"{os.path.abspath(os.path.dirname(os.path.realpath(__file__)))}"

game = Game(PROJECT_PATH)


# Gameplay funcs
def choose_random_ship():
    """Chooses a random ship and returns in stringname of the boat"""
    rand_ship = random.randint(0, 3)
    match rand_ship:
        case 0:
            chosen_ship = "battleship"
        case 1:
            chosen_ship = "cruiser"
        case 2:
            chosen_ship = "destroyer"
        case 3:
            chosen_ship = "uboat"
        case _:
            chosen_ship = "Unknown"
    return str(chosen_ship)


def place_all_ships(obj):
    """Regelt das plazieren aller Boote."""

    ships = obj.owner.get_ships()

    battleship = 1 - len(ships["battleship"])
    cruiser = 2 - len(ships["cruiser"])
    destroyer = 3 - len(ships["destroyer"])
    uboat = 4 - len(ships["uboat"])

    while (battleship + cruiser + destroyer + uboat) != 0:
        is_bot = obj.owner.get_bot()

        obj.show_boatfield()
        if is_bot is False:
            print(
                f"You have {battleship} Battleship (5-Long), {cruiser} Cruiser (4-Long), {destroyer} Destroyer (3-Long)"
                f" and {uboat} U-Boats (2-Long) availible!\nWhich Ship would you like to place?"
            )

            clear_input()
            current_boat_to_place = str(
                input("Please type in the boats name, or the length of it: ")
            ).lower()
        else:
            # Hier Schiffe automatisch plazieren
            current_boat_to_place = choose_random_ship()

        match current_boat_to_place:
            case "2" | "u-boat" | "uboat":
                if uboat > 0:
                    obj.set_ship(2, "uboat", is_bot)

                    uboat -= 1
                else:
                    print("You already placed all your U-Boats!")
            case "3" | "destroyer":
                if destroyer > 0:
                    obj.set_ship(3, "destroyer", is_bot)
                    destroyer -= 1
                else:
                    print("You already placed all your Destroyers!")
            case "4" | "cruiser":
                if cruiser > 0:
                    obj.set_ship(4, "cruiser", is_bot)
                    cruiser -= 1
                else:
                    print("You already placed all your Cruisers!")
            case "5" | "battleship":
                if battleship > 0:
                    obj.set_ship(5, "battleship", is_bot)
                    battleship -= 1
                else:
                    print("You already placed your Battleship!")
            case _:
                console_helper.clear_console()
                print(
                    f"{console_helper.BOLD}{console_helper.RED}Unknown Boat-Type.{console_helper.RESET}"
                )
        game.save_game()

    console_helper.clear_console()
    obj.show_boatfield()
    input(
        "You placed all your Boats! Your final Field looks like this. Press Enter to Continue!"
    )
    console_helper.clear_console()


def attack_execution(attacker, target):
    """Attacks the target and set target as new current_player"""
    status = "hit"
    while status == "hit":
        status = attacker.attack_enemy(target)
        game.save_game()
    if status == "win":
        ## DELETE FILE when game ends
        save_path = game.get_save_path()
        if os.path.exists(save_path):
            print(
                f"---------------------------------------------DELETE{save_path}\n---------------------------------------------"
            )
            shutil.rmtree(save_path)
        audio_process = simpleaudio.WaveObject.from_wave_file(
            f"{game.get_sound_path()}/winning.wav"
        )
        audio_process.play().wait_done()
        sys.exit()
    else:
        attacker.show_fields_side_by_side()
        game.set_last_turn_player(target)
        game.save_game()

        input(
            "You finished your Attack! Your final Fields looks like this. Press Enter to Continue!"
        )


# Game walkthrough
if __name__ == "__main__":
    players = game.get_players()

    if game.get_current_level() == 0:
        for index, player in enumerate(players):
            console_helper.clear_console()
            print(
                f"{console_helper.RED}Your Turn {player.owner.get_player_name()}!{console_helper.RESET}"
            )
            game.save_game()
            place_all_ships(player)
            player.show_boatfield()
            if index < len(players) - 1:
                game.set_last_turn_player(players[index + 1])
                game.save_game()
            else:
                game.set_last_turn_player(players[0])
                game.save_game()
        game.set_current_level(game.get_current_level() + 1)
        game.save_game()

    player_1 = players[0]
    player_2 = players[1]

    if game.get_current_level() == 1:
        while (player_1.get_ships_left() != 0) and (player_2.get_ships_left() != 0):
            console_helper.clear_console()
            print(
                f"{console_helper.RED}Your Turn {player_1.owner.get_player_name()}!{console_helper.RESET}"
            )
            player_1.show_fields_side_by_side()

            attack_execution(
                attacker=player_1,
                target=player_2,
            )

            console_helper.clear_console()
            print(
                f"{console_helper.RED}Your Turn {player_2.owner.get_player_name()}!{console_helper.RESET}"
            )
            player_2.show_fields_side_by_side()
            attack_execution(
                attacker=player_2,
                target=player_1,
            )
