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
RULES = SHEET.worksheet("rules")


def validate_menu_input(input_value):
    """
    makes all string data lower case and raises valueError if invalid data.
    """
    try:
        options_list = ["rules", "newgame", "continue"]
        if input_value.lower() not in options_list:
            raise ValueError(f"You must enter 1 of the 3 commands listed above. \
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


def validate_coordinate(coord, cell):
    """
    Validates the input coordinates when placing ships.
    """
    try:
        if len(coord) != 2:
            raise RuntimeError(
                f"{coord}. It should be a letter followed by a single number"
                )
        let = coord[0]
        num = coord[1]
        if let not in string.ascii_letters:
            raise RuntimeError(
                f"{coord}. The first character cannot be a number"
                )
        elif PLAYER.acell(let.upper() + str(int(num)+cell)).value is None:
            raise RuntimeError("You cannot place a ship outside of the grid")
        elif PLAYER.acell(let.upper() + str(int(num)+cell)).value != ".":
            raise RuntimeError("You cannot place a ship on another ship")
    except RuntimeError as e:
        print(f"\n\nInavlid coordinate selected: {e}, please try again.\n")
        return False
    return True


def validate_strike_coord(coord):
    """
    Validates the input coordinates when firing.
    """

    try:
        if len(coord) != 2:
            raise RuntimeError(
                f"{coord}. It should be a letter followed by a single number"
                )
        let = coord[0]
        num = coord[1]
        if let not in string.ascii_letters:
            raise RuntimeError(
                f"{coord}. The first character cannot be a number"
                )
        elif COMPUTER.acell(let.upper() + str(int(num))).value is None:
            raise RuntimeError("You cannot fire outside of the grid")
    except RuntimeError as e:
        print(f"\n\nInavlid coordinate selected: {e}, please try again.\n")
        return False
    return True


def check_game_resume(user):
    """
    Checks if any ship values from the sheet remain,
    and if not, prints a message.
    """
    if user == "player":
        if len(
            COMPUTER.findall("B")+COMPUTER.findall("C")+COMPUTER.findall("D")
                ) == 0:
            print("\n_________________________________________\
                \nYou have sunk all of the opponents ships!\
                \nCongratulations, YOU WIN!\
                \n_________________________________________\n\n")
            return False
    elif user == "computer":
        if len(
            PLAYER.findall("B")+PLAYER.findall("C")+PLAYER.findall("D")
                ) == 0:
            print("\n_________________________________________\
                \nAll of your ships have been sunk...\nYOU LOST!\
                \n_________________________________________\n\n")
            return False


def start_menu():
    """
    Prints the welcome message and input options on
    when file is run, and when called.
    """
    while True:
        print(f'\n\n{RULES.acell("A16").value}')
        print("\n\n                Welcome to Battleship!\n\n")
        print("The classic World War 1 game, running in your terminal!\n")
        print('Type one of the following commands below and hit enter:\n\
    "Rules",    "NewGame",    "Continue"')
        input_command = input("Enter command: \n")
        if validate_menu_input(input_command):
            break
    return input_command.lower()


def rules():
    """
    Prints the rules for how to play the game.
    """
    for i in range(1, 15):
        print(RULES.acell(f"A{i}").value)
    input("\n(Press any key and/or enter to return to the menu.)")
    print("\n\n")
    main()


def overwrite_current_game():
    """
    Checks if the user wants to overwrite the current game and validates input.
    """
    if COMPUTER.get_all_values() != []:
        while True:
            print("\nStarting a new game will overwrite your current game")
            input_val = input("Are you sure you want to proceed? Y/N: \n")
            if input_val.lower() in ["yes", "yeah", "y"]:
                print("Starting a new game...")
                break
            elif input_val.lower() in ["no", "nope", "n"]:
                print("Resuming previous game...")
                continue_game()
            else:
                print("You must enter either Yes / Y or No / N.")


def setup_grid(setup_list, user):
    """
    Clears the board, then adds a new grid.
    Pprints the grid if initiated by PLAYER.
    """
    user.clear()
    set_cols = ["." for x in range(setup_list[1])]
    set_grid = [set_cols for x in range(setup_list[0])]
    user.append_rows(set_grid)
    if user == "PLAYER":
        pprint(user.get_all_values())


def computer_pos_ships(setup_list):
    """
    First generates the computer grid, then places ships randomly.
    Then checks if ships were correctly placed on the grid, and if not,
    restarts the function and resets the grid. This loops until placement
    is correct, at which point the grid is used to update "COMPUTER".
    """
    grid = [["." for a in range(setup_list[1])] for a in range(setup_list[0])]
    for i in range(2, 5):
        for x in range(setup_list[i]):
            ship_type = {2: "Battleship", 3: "Cruiser", 4: "Destroyer"}
            ship_length = {2: 4, 3: 3, 4: 2}
            while True:
                rand_x = rand_int("x", setup_list, ship_length[i])
                rand_y = rand_int("y", setup_list, ship_length[i])
                for height in range(setup_list[0]):
                    if "." in grid[height][rand_x]:
                        for sl in range(ship_length[i]):
                            grid[(rand_y + sl)][rand_x] = ship_type[i][0]
                    break
                break

    dot_inst = 0
    for y in range(setup_list[0]):
        dot_inst = dot_inst + (grid[y].count("."))
    ship_inst = setup_list[0] * setup_list[1] - dot_inst
    max_ship_inst = 0
    for i in range(2, 5):
        max_ship_inst = max_ship_inst + setup_list[i] * ship_length[i]
    if ship_inst != max_ship_inst:
        computer_pos_ships(setup_list)
    else:
        print("Computer Ready!")
        COMPUTER.clear()
        # Lines 226 to 230 below are copied from external code. See readme.
        SHEET.values_update(
            'computer_board!A1',
            params={'valueInputOption': 'RAW'},
            body={'values': grid}
        )


def position_ships(setup_list):
    """
    First calls the setup grid function,
    then allows the user to place his ships within the defined grid.
    If an error is caught, restarts the whole function.
    """
    setup_grid(setup_list, PLAYER)
    setup_grid(setup_list, HIT_MAP)
    print('\nPlace your ships by entering the coordinate for the front of \
each ship.\nExample: "A1"')
    for i in range(2, 5):
        for x in range(setup_list[i]):
            ship_type = {2: "Battleship", 3: "Cruiser", 4: "Destroyer"}
            ship_length = {2: 4, 3: 3, 4: 2}
            coord = input(f"Place your {ship_type[i]}: \n")
            for cell in range(ship_length[i]):
                if validate_coordinate(coord, cell):
                    update = coord[0].upper() + str(int(coord[1])+cell)
                    PLAYER.update_acell(update, ship_type[i][0])
                else:
                    position_ships(setup_list)
            pprint(PLAYER.get_all_values())


def random_coordinate(grid_height, grid_width, ship_length):
    """
    Generates a random coordinate based on grid dimensions (uses
    ship length when generating numbers for computer ship positions,
    otherwise the function should be passed a shiplength of 1,
    in which case the function will return a "(0,0)" coordinate,
    and a "(A1)" coordinate).
    """
    if ship_length != 1:
        rand_num = random.randint(1, (grid_height - ship_length + 1))
        rand_let = string.ascii_letters[random.randint(1, grid_width) - 1]
        rand_coord = rand_let.upper() + str(rand_num)
    else:
        rand_y = random.randint(0, grid_height - 1)
        rand_x = random.randint(0, grid_width - 1)
        rand_num = rand_y + 1
        rand_let = string.ascii_letters[rand_x]
        rand_grid_coord = rand_let.upper() + str(rand_num)
        rand_coord = [rand_y, rand_x, rand_grid_coord]
    return rand_coord


def rand_int(val, setup_list, ship_length):
    """
    test
    """
    grid_height = setup_list[0]
    grid_width = setup_list[1]
    if val == "x":
        rand_x = random.randint(0, (grid_width - 1))
        return rand_x
    if val == "y":
        rand_y = random.randint(0, (grid_height - ship_length))
        return rand_y


def get_grid_dim():
    """
    Gets the grid dimensions from the player sheet and returns as a list.
    """
    height = len(PLAYER.get_all_values())
    width = len(PLAYER.get_all_values()[0])
    grid_dim = [int(height), int(width)]
    return grid_dim


def setup_newgame():
    """
    Request input for board size and passes it and ships to position_ships().
    """
    overwrite_current_game()
    while True:
        print("\nPlease define the game parameters:")
        grid_height = input("Grid height (5-9): \n")
        grid_width = input("Grid width (5-9): \n")
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
    wave = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    if validate_strike_coord(coord):
        cell = coord[0].upper() + str(int(coord[1]))
        if COMPUTER.acell(cell).value == ".":
            COMPUTER.update_acell(cell, "X")
            HIT_MAP.update_acell(cell, "o")
            print(f"\n{cell} was a miss!\n{wave}")
        elif COMPUTER.acell(cell).value == "X":
            print(f"You had already fired at {cell}... Too bad.\n{wave}")
        else:
            COMPUTER.update_acell(cell, "X")
            HIT_MAP.update_acell(cell, "X")
            print(f"\n{cell} was a hit!\n{wave}")
    else:
        continue_game()


def computer_turn(rand_cell):
    """
    Takes the coordinate passed and updates the player sheet.
    Prints a message, then pretty prints the player's sheet.
    """
    print("Your grid:")
    grid = PLAYER.get_all_values()
    rand_y = rand_cell[0]
    rand_x = rand_cell[1]

    while True:
        if grid[rand_y][rand_x] == ".":
            PLAYER.update_acell(rand_cell[2], "o")
            pprint(PLAYER.get_all_values())
            print(f"Computer fired at {rand_cell[2]} and missed!")
            break
        elif grid[rand_y][rand_x] == "o":
            continue
        else:
            PLAYER.update_acell(rand_cell[2], "X")
            pprint(PLAYER.get_all_values())
            print(f"\nComputer fired at {rand_cell[2]} and hit!")
            break


def continue_game():
    """
    Gets the current game from the spreadsheets.
    If no current game is available, asks user to start new game.
    Resumes at player's turn. Validates player input,
    then checks if the game is over,
    Plays the computer's turn, checks if the game is over,
    and if not, repeats.
    """
    if COMPUTER.get_all_values() != []:
        while True:
            print("\nOpponents grid:")
            pprint(HIT_MAP.get_all_values())
            cell = input("Your turn. Enter coordinate to hit: \n")
            player_turn(cell)
            cont = check_game_resume("player")
            if cont is False:
                break

            grid_dim = get_grid_dim()
            rand_cell = random_coordinate(grid_dim[0], grid_dim[1], 1)
            while PLAYER.acell(rand_cell[2]).value == "X":
                rand_cell = random_coordinate(grid_dim[0], grid_dim[1], 1)
            computer_turn(rand_cell)
            cont = check_game_resume("computer")
            if cont is False:
                break
        PLAYER.clear()
        COMPUTER.clear()
        HIT_MAP.clear()
    else:
        print("\nNo current game to resume...\nReturning to menu.\n")
        main()


def main():
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
        main()
    computer_pos_ships(setup_list)
    position_ships(setup_list)
    continue_game()
    main()


main()
