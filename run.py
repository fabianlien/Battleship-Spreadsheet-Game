import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
import random

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('battleship')
PLAYER = SHEET.worksheet('player_board')
COMPUTER = SHEET.worksheet('computer_board')


print('Welcome to "Battleship"')
print("The classic World War 1 game, running directly in your terminal!\n")
print('Type one of the following commands below and hit enter:\
  "Rules",  "NewGame",  "Score",  "Forfeit"')
input_command = input("Enter command: ")


def rules():
    """
    Prints the rules for how to play the game.
    """
    print("insert rules string here...")


def setup_grid(setup_list, user):
    """
    Clears the board, then adds a new grid,
    Pprints the grid if initiated by PLAYER.
    """
    user.clear()
    set_cols = ["." for x in range(setup_list[1])]
    set_grid = [set_cols for x in range(setup_list[0])]
    user.append_rows(set_grid)
    if user == "PLAYER":
        pprint(user.get_all_values())


def position_ships(setup_list):
    """
    First calls the setup grid function,
    then allows the user to place his ships within the defined grid.
    """
    setup_grid(setup_list, PLAYER)

    print("Place your ships by entering the coordinate for the front of each \
ship.")
    for i in range(setup_list[2]):
        coordinate = input("Place your Battleship: ")
        let = coordinate[0]
        num = coordinate[1]
        for cell in range(4):
            if PLAYER.acell(let.upper() + str(int(num)+cell)).value == ".":
                PLAYER.update_acell(let.upper() + str(int(num)+cell), "B")
            elif PLAYER.acell(let.upper() + str(int(num)+cell)).value is None:
                print("You cannot place a ship outside of the game grid\n.")
                position_ships(setup_list)
            else:
                print("You cannot place a ship on another ship.\n")
                position_ships(setup_list)
        pprint(PLAYER.get_all_values())

    for i in range(setup_list[3]):
        coordinate = input("Place your Cruiser: ")
        let = coordinate[0]
        num = coordinate[1]
        for cell in range(3):
            if PLAYER.acell(let.upper() + str(int(num) + cell)).value == ".":
                PLAYER.update_acell(let.upper() + str(int(num) + cell), "C")
            elif PLAYER.acell(let.upper() + str(int(num)+cell)).value is None:
                print("You cannot place a ship outside of the game grid.\n")
                position_ships(setup_list)
            else:
                print("You cannot place a ship on another ship.\n")
                position_ships(setup_list)
        pprint(PLAYER.get_all_values())

    for i in range(setup_list[3]):
        coordinate = input("Place your Destroyer: ")
        let = coordinate[0]
        num = coordinate[1]
        for cell in range(2):
            if PLAYER.acell(let.upper() + str(int(num) + cell)).value == ".":
                PLAYER.update_acell(let.upper() + str(int(num) + cell), "D")
            elif PLAYER.acell(let.upper() + str(int(num)+cell)).value is None:
                print("You cannot place a ship outside of the game grid.\n")
                position_ships(setup_list)
            else:
                print("You cannot place a ship on another ship.\n")
                position_ships(setup_list)
        pprint(PLAYER.get_all_values())


def computer_pos_ships(setup_list):
    """
    Generates the computer grid and places ships randomly.
    """
    setup_grid(setup_list, COMPUTER)
    rand_num = random.randint(0, setup_list[0])
    print(rand_num)


def setup_newgame():
    """
    Request input for board size and passes it and ships to position_ships().
    """
    print("\nPlease define the game parameters:")
    grid_height = int(input("Grid height (5-10): "))
    grid_width = int(input("Grid width (5-10): "))
    try:
        if grid_height < 5 or grid_width < 5:
            print("\nThe grid is too small. Both width and height must be \
at least 5.")
            setup_newgame()
        elif grid_height * grid_width <= 36:
            print("Your armada contains:\n\
            1 Battleship (length 4)\n\
            2 Cruisers (length 3)\n\
            2 Destroyers (length 2)")
            setup_list = [grid_height, grid_width, 1, 2, 2]
            return setup_list
        elif grid_height * grid_width <= 64:
            print("Your armada contains:\n\
            2 Battleships (length 4)\n\
            3 Cruisers (length 3)\n\
            3 Destroyers (length 2)")
            setup_list = [grid_height, grid_width, 2, 3, 3]
            return setup_list
        elif grid_height * grid_width < 99:
            print("Your armada contains:\n\
            3 Battleships (length 4)\n\
            3 Cruisers (length 3)\n\
            5 Destroyers (length 2)")
            setup_list = [grid_height, grid_width, 3, 3, 5]
            return setup_list
        elif grid_height > 10 or grid_width > 10:
            print("\nThe grid is too big. Both width and height must be \
less than 10.")
            setup_newgame()
    finally:
        position_ships(setup_list)


def print_current_score():
    """
    Print current scores to terminal.
    """


def forfeit_y_n():
    """
    Asks the user if they want to forfeit and either resets the game or
    continues.
    """
    option = input("Are you sure you want to forfeit? Yes/No: ")
    if list(option)[0].lower() == "y":
        print("You lost.")
    elif list(option)[0].lower() == "n":
        print("Resume game:")
    else:
        raise ValueError(f"{option} is not a valid answer.")


def validate_input(input_value):
    """
    makes all string data lower case and raises valueError if invalid data.
    """
    if input_value.lower() == "rules":
        rules()
    elif input_value.lower() == "newgame":
        setup_list = setup_newgame()
        return setup_list
    elif input_value.lower() == "score":
        print_current_score()
    elif input_value.lower() == "forfeit":
        forfeit_y_n()
    else:
        raise ValueError(f"Unknown command {input_value}")


def main():
    """
    Run all program functions
    """
    setup = validate_input(input_command)
    computer_pos_ships(setup)


main()
