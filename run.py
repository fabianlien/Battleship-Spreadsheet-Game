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


def setup_newgame():
    """
    Request input for board size and ships and passes it to new game function.
    """
    print("newgame setup function")


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
