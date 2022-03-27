# BATTLESHIP

This is a python-based console version of the classic world war I game "Battleship". It has been deployed to a Heroku mock terminal.

[Here is a link to the live project.](insert url here!)

The objective of the game is simple: sink all of your opponents ships before the opponent sinks yours. In this version of the game you play against the computer in the terminal.

## How to play:
*Below are instructions for how the game works, which have been copied from the game itself:*

1. Before the game starts each player recieves a certain amount of ships depending on the size of the grid. The exact ships can be seen with their corresponding grid size below:
   * Shiptypes (lengths): Battleship (4 Coordinates), Cruiser (3 coordinates), Destroyer (2 coordinates)
   * For grids with up to 36 coordinates you recieve: 1 Battleship, 1 Cruiser, 2 Destroyers.
   * For grids with up to 64 coordinates you recieve: 2 Battleships, 3 Cruisers, 3 Destroyers.
   * For grids with up to 64 coordinates you recieve: 2 Battleships, 3 Cruisers, 3 Destroyers.
2. After you have recieved your ships you must place them on the grid. This is done by one at a time typing in the desired coordinate for the front of each ship. Ships align vertically.
   * Ships cannot be placed so that they overlap eachother, and must be placed entirely within the grid.
3. Once all the ships have been placed the game begins with the player selecting an enemy coordinate within the grid to fire upon.
   * If the coordinate contains an enemy ship you will recieve a notice that the strike was a hit, otherwise you will be informed that it was a miss.
   * After ther strike a "hit map" showing the strikes on the enemy grid will appear, this will help you keep track of your previous strikes. 
4. Your oponent will now select a coordinate and perform a strike. You will be able to see your opponents strikes after each turn on your own grid.
5. The game continues until all the coordinates containing ships in either grid have been hit. At this point the winner is declared and the game ends.

## Features:

### Existing Features:
* **Main Menu:**  
Upon running the game the user is presented with an input that allows for 3 options:
   - **"Rules"** - Loads the same text as seen above for users that are not familiar with the game.
   - **"NewGame"** - Provides the user with input fields to set up the parameters for a new game.
   - **"Continue"** - Allows the user to resume a previous game. Since the terminal only has access to the RAM and no other local storage, the game has been configured to store the data from the ongoing game in a spreadsheet grid (using Google Sheets and the gspread API.)

* **Grid Configuration:**  
When a new game is initiated the player is allowed to decide the grid dimensions between 5 and 9 coordinates long and wide. Subsequently the amount of ships available is determined by the size of the grid (specified in the rules above).

* **Different Ship Types:**  
The game contains three different types of ships, which each have different lengths, making the guessing a bit harder for the user. The ship specifications can be found with the game "Rules".

* **Dynamic Battleship Placement:**  
Following the set up of the grid, the computer will randomly (using the "random" python library) set up its ships on the grid. The player, on the other hand, gets to place their ships manually. Just as in the traditional version of the game - the ships have to be placed entirely within the grid, and cannot overlap with one another!

* **Alphanumeric Coordinate Input:**  
The game allows the user to enter coordinates using the so called Atlas grid system. Just as you would when playing with pen and paper!

* **Board Displays:**  
Rather than being all text based, each turn the grid is printed to the terminal as nested lists in the shape of a table using Pythons Pretty Print. This allows the user to easily keep track of where both they, and the computer has fired.

* **Input Validation:**  
The game uses a series of validator functions to catch errors from incorrect inputs in order to prevent the game from crashing. To help the user, the validators print comments to the terminal telling the user what they did wrong.

## Future Features to Implement:
* **Horisontal Ship Placement:**  
Currently it is only possible to place the ships vertically in the grid. Being able to alternate with horisontal placement would make the game much more dynamic for the user.
* **Point System:**  
Using gspread for storage in google sheets would allow for the user to save scores from previous games after closing the terminal.
* **PLAYER vs. PLAYER**
The biggest feature would be the ability to play against another person using a second terminal. This future about would indeed be possible since the 2 terminals could easilt share an external sheet.

## Data Modelling:  
The python code is written as a series of granular function blocks of which there is a logic flow running through a main function as a final code block. Each block contains a docstring describing its specific purpose. Validation takes place in seperate functions in order to make code more readable. Where possible, the code has been refactored so as to reduce the repetition of code.

## Testing:  
All testing of this project has been done manually by running the game in the local terminal. In addition to the built in debugging tools, the code has also passed through a PEP8 linter, which confirmed that there where no syntax errors.

## Solved Bugs:  
* There was an issue with the placement of the ships where the computer would not place the ships within the grid. This was caused by the fact that when a ship was placed only the first (top) coordinate was check to see if it was within the grid. This was solved by factoring in logic that took account for each ships specific length.

* There was a problem which raised an error from the gspread API when sending too many requests over a short period of time to the external sheet. This occured towards the end of the game when the computer would loop continuosly until it found a coordinate it had not yet fired upon. This issue was solved by having the computer generate its own grid from the sheet and loop against it localy instead of sending a request for each iteration. It also greatly decreased the time elapsed for the computers turn.

## Unsolved Bugs:
* There is an error when validating the coordinate input, which is not being handled by the validator. If the user input is not only one character an IndexError is thrown (or if it is two characters but they are not a string and an integer in that order gspread throws an error). This occurs because the value passed to the validator requires atleast to 1 letter and 1 number to be indexed and the latter converted to an integer so that it can be validated against the API. A possible solution would be to use *args.

* During extensive manual testing a seemingly infinite loop would sometimes occur when the computer was carrying out its turn. Manual debugging and online troubleshooting have unfortunately not provided any solution or indication as to what the cuase may be.

* Another validator error occurs when the correct input is entered after having incorrectly entered other input. This causes the validator to raise an error as if the the data entered was the same data that was entered the first time. This bug is probably cuased by the nested loops within specific functions, and might be resolved by analyzing the exakt "breaking points" in the loops.

## Deployment:  
This project was deployed using Code Institute's mock terminal for Heroku.
The steps neccesary for deployment are as follows:
* Fork or clone this repository
* Create a new app in your Heroku account
* Set the buildbacks to *Python* and *NodeJS* (in that order!)
* Link the Heroku app to the repository
* Click *Deploy*

## Credits:
Troubleshooting and tutorials:  
[Stack Overflow](https://stackoverflow.com/)  
[W3 Schools](https://www.w3schools.com/python/)  
[Techie Delight](https://www.techiedelight.com/)

Media:  
[ASCII Artwork](https://www.asciiart.eu/vehicles/navy)





