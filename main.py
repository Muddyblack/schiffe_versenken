"""This is the main module where the entire game logic gets merged"""
import os
import sys
import time
import shutil
import random
import simpleaudio
from Library import console_helper
from Library import keyboard_helper
from Library import random_helper
from Library import game_paths


from Classes.game import Game

random.seed(time.time())


# Gameplay funcs
def left_to_place_ships(ship_types, ships):
    """
    - Walks through the preferences of ships
    - Returns the text to print and the amount of ships that are left to be placed

    """

    print_text = "You have\n"
    ships_left = 0
    placed_ships = []

    for ind, (key, value) in enumerate(ship_types.items(), start=1):
        ships_of_type_left = int(value["max"]) - len(ships[key])
        ships_left += ships_of_type_left

        if ships_of_type_left > 0:
            ship_num_col = console_helper.GREEN
        else:
            ship_num_col = console_helper.RED
            placed_ships.append(ind)

        print_text += f"{ind}: {key} {ship_num_col}{ships_of_type_left}{console_helper.RESET} ({value['length']}-Long)\n"

    # removing last comma and space
    print_text = print_text[: len(print_text) - 2].strip()

    return (
        f"{print_text}\n\nWhich Ship would you like to place?",
        ships_left,
        placed_ships,
    )


def place_all_ships(obj):
    """Manages the placement of all ships for the player/bot"""

    # gets the allowed ships and their settings as dictionary
    ship_types = obj.owner.get_ship_preferences()

    is_bot = obj.owner.get_bot()

    # Loop until all ships have beenn placed
    while True:
        ships = obj.owner.get_ships()

        left_ships = left_to_place_ships(ship_types, ships)
        left_ships_txt = left_ships[0]
        left_ships_num = left_ships[1]
        placed_ships = left_ships[2]

        # Exiting loop when no ship left to place
        if left_ships_num == 0:
            break

        # Getting bot/user input what ship should be set.
        if is_bot is False:
            # Get Input from User

            obj.show_boatfield()
            print(left_ships_txt)

            keyboard_helper.clear_input()
            current_boat_to_place = (
                input(
                    f"Please type in the boats {console_helper.LIGHT_WHITE}index{console_helper.RESET}, "
                    + f"or its {console_helper.LIGHT_WHITE}name{console_helper.RESET}: "
                )
                .lower()
                .strip()
            )
        else:
            # Get input from bot

            current_boat_to_place = random_helper.randint_exc(
                1, len(ship_types), placed_ships
            )

        # Getting the boat name if input was an integer
        # And looking if input is an Ingame-Object
        try:
            if (
                str(current_boat_to_place).isdigit()
                and int(current_boat_to_place) > 0
                and int(current_boat_to_place) <= len(ship_types)
            ):
                current_boat_to_place = list(ship_types.keys())[
                    int(current_boat_to_place) - 1
                ]

            curr_ship_type = ship_types[current_boat_to_place]
        except (KeyError, ValueError):
            console_helper.clear_console()
            print(
                f"{console_helper.BOLD}{console_helper.RED}Unknown Boat-Type.{console_helper.RESET}"
            )
            time.sleep(0.25)
            continue

        # Placing the ship
        if (int(curr_ship_type["max"]) - len(ships[current_boat_to_place])) > 0:
            ship_placed = obj.set_ship(
                curr_ship_type["length"], current_boat_to_place, is_bot
            )
            # If placing the ship did not work, then the game board is impossible.
            # In that case the placed ships get resettet and we start from scratch placing the ships
            if not ship_placed:
                obj.set_boatfield(obj.init_field())
                obj.owner.set_ships(obj.owner.init_ships())
                game.save_game()

                print(
                    f"{console_helper.RED}------------------------------------------------------\n"
                    + "IF THIS LOOP DOES NOT FINISH RESTART THE GAME"
                    + f"\n------------------------------------------------------\n{console_helper.RESET}"
                )
                time.sleep(3)

            if ship_placed and not is_bot:
                simpleaudio.WaveObject.from_wave_file(
                    f"{game_paths.SOUND_PATH}/Set-Ship.wav"
                ).play()
        else:
            print(
                f"{console_helper.RED}You already placed all your {current_boat_to_place}!{console_helper.RESET}"
            )
            time.sleep(0.35)

        game.save_game()
        console_helper.clear_console()

    if is_bot is False:
        obj.show_boatfield()
        input(
            "You placed all your Boats! Your final Field looks like this. Press Enter to Continue!Press Enter to Continue!"
        )
    else:
        input("The Bot placed all his ships. Press Enter to Continue!")
    console_helper.clear_console()


def attack_execution(attacker, target):
    """Attacks the target and sets target as new current_player"""

    status = "hit"

    if attacker.owner.get_bot() is False:
        attacker.show_fields_side_by_side()

    while status == "hit":
        status = attacker.attack_enemy(target)
        game.save_game()

        # playing audio depending on the status
        if status == "hit":
            simpleaudio.WaveObject.from_wave_file(
                f"{game_paths.SOUND_PATH}/HIT.wav"
            ).play()
        elif status == "water":
            simpleaudio.WaveObject.from_wave_file(
                f"{game_paths.SOUND_PATH}/Water-Drop.wav"
            ).play()

        time.sleep(0.1)

    if status == "win":
        ## DELETE FILE when game ends and play winning sound

        save_path = game.get_save_path()
        if os.path.exists(save_path):
            print(
                f"---------------------------------------------DELETE{save_path}\n---------------------------------------------"
            )
            shutil.rmtree(save_path)

        simpleaudio.WaveObject.from_wave_file(
            f"{game_paths.SOUND_PATH}/winning.wav"
        ).play().wait_done()

        ##EXITIING the script
        sys.exit()
    else:
        # End the function saving and waiting for User to continue
        game.set_last_turn_player(target)
        game.save_game()

        if attacker.owner.get_bot() is False:
            console_helper.clear_console()
            attacker.show_fields_side_by_side()
            input(
                "You finished your Attack! Your final Fields looks like this. Press Enter to Continue!"
            )
        else:
            input("The Bot finished his attack. Press Enter to Continue!")


# Game walkthrough
if __name__ == "__main__":
    # Setup the Game
    game = Game()
    players = game.get_players()

    # Walking through players and letting place their ships
    if game.get_current_level() == 0:
        for index, player in enumerate(players):
            console_helper.clear_console()
            print(
                f"{console_helper.RED}Your Turn {player.owner.get_player_name()}!{console_helper.RESET}"
            )

            game.save_game()
            place_all_ships(player)

            if player.owner.get_bot() is False:
                player.show_boatfield()

            if index < (len(players) - 1):
                game.set_last_turn_player(players[index + 1])
                game.save_game()
            else:
                game.set_last_turn_player(players[0])
                game.save_game()

        game.set_current_level(game.get_current_level() + 1)
        game.save_game()

    # Starting the Attacking loop until one player wins

    if game.get_current_level() == 1:
        while True:
            for index, player in enumerate(players):
                if index < (len(players) - 1):
                    next_p = players[index + 1]
                else:
                    next_p = players[0]

                console_helper.clear_console()
                print(
                    f"{console_helper.BROWN}Your Turn {player.owner.get_player_name()}!{console_helper.RESET}"
                )
                attack_execution(attacker=player, target=next_p)
