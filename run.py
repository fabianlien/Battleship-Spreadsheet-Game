import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
import random
import string

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("battleship")
PLAYER = SHEET.worksheet("player_board")
COMPUTER = SHEET.worksheet("computer_board")
HIT_MAP = SHEET.worksheet("hit_board")


def validate_menu_input(input_value):
    """
    makes all string data lower case and raises valueError if invalid data.
    """
    try:
        options_list = ["rules", "newgame", "continue", "forfeit"]
        if input_value.lower() not in options_list:
            raise ValueError(f"You must enter 1 of the 4 commands listed above. \
You entered {input_value}")
    except ValueError as e:
        print(f"\n\nInvalid input: {e}, please try again.\n")
        return False
    return True


def validate_grid_len(height, width):
    """
    Turns input from calling function to an integer and checks it value.
    """
    try:
        valid_height = int(height)
        valid_width = int(width)
        valid_height_coordinate = (valid_height > 4) and (valid_height < 10)
        valid_width_coordinate = (valid_width > 4) and (valid_width < 10)
        if valid_height_coordinate and valid_width_coordinate:
            return True
        else:
            error_message = "Your grid must be at least 5*5 and 9*9 at most"
            print(f"\nInvalid data type: {error_message}, please try again.\n")
            return False
    except ValueError:
        error_message = "The grid can only be comprised of numbers"
        print(f"\n\nInvalid data type: {error_message}, please try again.\n")
        return False


def validate_coordinate(coordinate, cell):
    """
    Validates the input coordinates when placing ships.
    """
    let = coordinate[0]
    num = coordinate[1]
    try:
        if len(coordinate) != 2:
            raise RuntimeError(
                f"{coordinate}. It should be a letter followed by a number"
                )
        elif PLAYER.acell(let.upper() + str(int(num)+cell)).value is None:
            raise RuntimeError("You cannot place a ship outside of the grid")
        elif PLAYER.acell(let.upper() + str(int(num)+cell)).value != ".":
            raise RuntimeError("You canot place a ship on another ship")
    except RuntimeError as e:
        print(f"\n\nInavlid coordinate selected: {e}, please try again.\n")
        return False
    return True


def validate_strike_coord(coordinate):
    """
    Validates the input coordinates when firing.
    """
    let = coordinate[0]
    num = coordinate[1]
    try:
        if len(coordinate) != 2:
            raise RuntimeError(
                f"{coordinate}. It should be a letter followed by a number"
                )
        elif COMPUTER.acell(let.upper() + str(int(num))).value is None:
            raise RuntimeError("You cannot fire outside of the grid")
    except RuntimeError as e:
        print(f"\n\nInavlid coordinate selected: {e}, please try again.\n")
        return False
    return True


def start_menu():
    """
    Prints the welcome message and input options on
    when file is first excecuted.
    """
    while True:
        print('Welcome to "Battleship"')
        print("The classic World War 1 game, running in your terminal!\n")
        print('Type one of the following commands below and hit enter:\
    "Rules",  "NewGame",  "Continue",  "Forfeit"')
        input_command = input("Enter command: ")
        if validate_menu_input(input_command):
            break
    return input_command.lower()


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
    If an error is caught, restarts the whole function.
    """
    setup_grid(setup_list, PLAYER)
    print("Place your ships by entering the coordinate for the front of \
each ship.")
    for i in range(2, 5):
        for x in range(setup_list[i]):
            ship_type = {2: "Battleship", 3: "Cruiser", 4: "Destroyer"}
            ship_length = {2: 4, 3: 3, 4: 2}
            coord = input(f"Place your {ship_type[i]}: ")
            for cell in range(ship_length[i]):
                if validate_coordinate(coord, cell):
                    update = coord[0].upper() + str(int(coord[1])+cell)
                    PLAYER.update_acell(update, ship_type[i][0])
                else:
                    position_ships(setup_list)
            pprint(PLAYER.get_all_values())


def random_coordinate(grid_height, grid_width, ship_length):
    """
    Generates a random coordinate based on grid dimensions.
    """
    rand_num = random.randint(1, (grid_height - ship_length + 1))
    rand_let = string.ascii_letters[random.randint(1, grid_width - 1)]
    rand_coord = rand_let.upper() + str(rand_num)
    return rand_coord


def get_grid_dim():
    """
    Gets the grid dimensions from the player sheet and returns as a list.
    """
    height = len(PLAYER.get_all_values())
    width = len(PLAYER.get_all_values()[0])
    grid_dim = [int(height), int(width)]
    return grid_dim


def computer_pos_ships(setup_list):
    """
    First generates the computer and hit map grids, then places ships randomly.
    """
    setup_grid(setup_list, COMPUTER)
    setup_grid(setup_list, HIT_MAP)
    ship_length = 4

    for i in range(3):
        r_c = random_coordinate(setup_list[0], setup_list[1], ship_length)
        print(r_c)
        if COMPUTER.acell(r_c).value == ".":
            for x in range(ship_length):
                COMPUTER.update_acell((r_c[0].upper() + str(int(r_c[1])+x)), "B")


    #for i in range(2, 5):
    #    for x in range(setup_list[i]):
    #        ship_type = {2: "Battleship", 3: "Cruiser", 4: "Destroyer"}
    #        ship_length = {2: 4, 3: 3, 4: 2}
    #        r_c = random_coordinate(setup_list[0], setup_list[1])
    #        for cell in range(ship_length[i]):
    #            if COMPUTER.acell(r_c[0].upper() + str(int(r_c[1])+cell)).value == ".":
    #                update = r_c[0].upper() + str(int(r_c[1])+cell)
    #                COMPUTER.update_acell(update, ship_type[i][0])
    #            else:
    #                random_coordinate(setup_list[0], setup_list[1])

    #COMPUTER.update_acell(r_c[0].upper() + str(int(r_c[1])+cell), ship_type[i][0])
                #update = r_c[0].upper() + str(int(r_c[1])+cell)
                #COMPUTER.update_acell(update, ship_type[i][0])

    print("Computer Ready!")


def setup_newgame():
    """
    Request input for board size and passes it and ships to position_ships().
    """
    while True:
        print("\nPlease define the game parameters:")
        grid_height = input("Grid height (5-9): ")
        grid_width = input("Grid width (5-9): ")
        if validate_grid_len(grid_height, grid_width):
            break
    grid_height = int(grid_height)
    grid_width = int(grid_width)
    num_l = [[36, 1, 1, 2], [64, 2, 3, 3], [81, 3, 3, 5]]
    for i in range(3):
        if grid_height * grid_width <= num_l[i][0]:
            print(f"Your armada contains:\n\
            {num_l[i][1]} Battleships (length 4)\n\
            {num_l[i][2]} Cruisers (length 3)\n\
            {num_l[i][3]} Destroyers (length 2)")
            setup_list = [
                grid_height, grid_width, num_l[i][1], num_l[i][2], num_l[i][3]
                ]
            return setup_list


def player_turn(coord):
    """
    Takes the coordinate passed and checks if the target is valid,
    Then updates the hit map and computer sheets annd prints a message.
    Finally pretty prints the hitmap.
    """
    if validate_strike_coord(coord):
        cell = coord[0].upper() + str(int(coord[1]))
        if COMPUTER.acell(cell).value == ".":
            COMPUTER.update_acell(cell, "X")
            HIT_MAP.update_acell(cell, "o")
            print(f"\n{cell} was a miss!\n")
        elif COMPUTER.acell(cell).value == "X":
            print("You have already fired there... Too bad.")
        else:
            COMPUTER.update_acell(cell, "X")
            HIT_MAP.update_acell(cell, "X")
            print(f"\n{cell} was a hit!\n")
    else:
        continue_game()


def computer_turn(rand_cell):
    """
    Takes the coordinate passed and updates the player sheet.
    Prints a message then pretty prints the player's sheet.
    """
    if PLAYER.acell(rand_cell).value == ".":
        PLAYER.update_acell(rand_cell, "X")
        print(f"Computer fired at {rand_cell} and missed!\n")
    else:
        PLAYER.update_acell(rand_cell, "X")
        print(f"\nComputer fired at {rand_cell} and hit!\n")
    pprint(PLAYER.get_all_values())


def continue_game():
    """
    Gets the current game from the spreadsheets and resumes at player's turn.
    Plays the computer's turn, then validates if the game is over,
    and if not, function calls itself again.
    """
    print("\n")
    pprint(HIT_MAP.get_all_values())
    cell = input("Your turn. Enter coordinate to hit: ")
    player_turn(cell)

    grid_dim = get_grid_dim()
    rand_cell = random_coordinate(grid_dim[0], grid_dim[1], 1)
    while PLAYER.acell(rand_cell).value == "X":
        rand_cell = random_coordinate(5, 5, 1)
    computer_turn(rand_cell)
    #add validator to see if game is over.
    continue_game()


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


def setup():
    """
    Run all program functions
    """
    start_menu_input = start_menu()
    validate_menu_input(start_menu_input)
    if start_menu_input == "rules":
        rules()
    elif start_menu_input == "newgame":
        setup_list = setup_newgame()
    elif start_menu_input == "continue":
        continue_game()
    elif start_menu_input == "forfeit":
        forfeit_y_n()
    computer_pos_ships(setup_list)
    position_ships(setup_list)
    continue_game()


get_grid_dim()
setup()
