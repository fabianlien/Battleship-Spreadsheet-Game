import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('battleship')
PLAYER_BOARD = SHEET.worksheet('player_board')
COMPUTER_BOARD = SHEET.worksheet('computer_board')

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


def position_ships(setup_list):
    """
    Allows the user to place his ships within the defined grid.
    """
    print(f"Choose where to place your ships by entering their coordinates \
seperated by commas. {setup_list}")


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
        elif grid_height * grid_width <= 100:
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
        setup_newgame()
    elif input_value.lower() == "score":
        print_current_score()
    elif input_value.lower() == "forfeit":
        forfeit_y_n()
    else:
        raise ValueError(f"Unknown command {input_value}")


validate_input(input_command)
