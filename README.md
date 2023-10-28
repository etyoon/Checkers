# Checkers Project
Title: Checkers <br />
CS 142 - 2023 WINTER <br />
Made by: Soyoon Moon, Jiyeong Lee, David Ma, Ethan Yoon <br />

In this project we made checkers board that two players can play. There is also option to play with a bot (smart or random bot). GUI and TUI are also implemented to improve user experience. <br />

```checkers.py``` (David Ma): Code that includes logic for checkers game <br />
```bot.py``` (Jiyeong Lee): Code for smart and random bot that plays checkers against the human player <br />
```gui.py``` (Soyoon Moon): GUI implementation for the checkers game <br />
```tui.py``` (Ethan Yoon): TUI implementation for the checkers game <br />

## Set-Up
Running the code in this repository requires using a number of Python libraries.

To install the required Python libraries, run the following from the root of the repository:
```
pip3 install -r requirements.txt
```

## Running the TUI
To run the TUI, ensure that all required packages listed in requirements.txt are installed. Then, run the following from the root of the repository: <br />
```
python3 src/tui.py --board-size <int>
```
Where ```<int>``` is an integer for the size of the board, if left out the default integer is 3

The TUI displays the state of the board and asks for a row number (starting at zero) then column number (starting at zero) of a piece. Then, a player must select a highlighted possible moves (displayed on the terminal in a numbered list) before moving the corresponding piece to the corresponding move. If a jumping move must be made, the player can only choose from those possible jumping moves. If a player wishes to resign or request a draw, the player may input 'resign' or 'draw' on their turn.  <br />

You can also play against a bot like this: <br />
```
python3 src/tui.py --player2 <bot>
```
Where ```<bot>``` is either ```random-bot``` or ```smart-bot``` (the bots are described further below). <br />
You can even have two bots play against each other:
```
python3 src/tui.py --player1 <bot> --player2 <bot>
python3 src/tui.py --player1 random-bot --player2 smart-bot --board-size 4
```

## Running the GUI
To run the GUI, you must be inside the src. Run the following from the root of the repository (!!this is important!! You need to be inside /src to run it!):
```
cd src/
```
Then, run the following from the src of the repository:
```
python3 gui.py --board-size <int>
```
Where ```<int>``` is an integer for the size of the board, if left out the default integer is 3

The GUI displays the state of the board. The player can click on a piece to see its immediate possible moves highlighted. Dragging the mouse to that destination square moves the piece. <br />

Like the TUI, you can play against a bot, or have two bots play against each other like this:
```
python3 gui.py --player2 <bot>
python3 gui.py --player1 <bot> --player2 <bot>
python3 gui.py --player1 smart-bot --player2 smart-bot --board-size 3
```

## Bots
The ```bots.py``` file includes two classes: <br />
* ```RandomBot```: A bot that will just choose a move (or accept a draw request) at random <br />
* ```SmartBot```: Using an alpha-beta pruning method on a minimax algorithm, it will keep
    track of possible plays (until a player wins or up to depth of 5) that
    result from making certain moves. The last state of the board at each play
    is evaluated to determine how favorable the play is for the bot. The
    methodology for the evaluation is as follows (adapted from website cited
    above). When the opponent requests a draw, the bot accepts only if the board is no longer favorable for the bot. <br />
        - Who has more/better pieces? Kings are worth 5000, normal pieces are
        worth 3000. <br />
        - Whose pieces are, on average, closer to being kings? The closeness of
        each non-king pieces are added (the higher the number, the clower the
        piece is to being a king). An average of this sum is multiplied by 10.
        - A total of these two categories are added for each player. <br />
        - The opponent's evaluation score is subtracted from the bot's
        evaluation score to determine the evaluation number for the state of
        the board. <br />

These two classes are used in the TUI and GUI, but you can also run ```bots.py``` to run 100 simulated games where two bots face each other, and see the percentage of wins and ties. <br />
For Example:
```
$ python3 src/bot.py --player1 random --player2 random
Bot 1 (random) wins: 46.00%
Bot 2 (random) wins: 45.00%
Ties: 9.00%

$ python3 src/bot.py --player1 random --player2 smart
Bot 1 (random) wins: 4.00%
Bot 2 (smart) wins: 92.00%
Ties: 4.00%
```
You can control the number of simlated games using the ```-n <number of games>``` parameter to ```bots.py```

## Developments since Milestones 1 and 2 for ```checkers.py```
#### Milestone 1
1. We switched from using integers 0 and 1 to using an Enum class with values 0 and 1 to represent top and bottom players on the board.
2. Implemented design feedback that recommended making the Board class generalize to m by n board sizes rather than simple square n by n board sizes.
3. Implemented design feedback that suggested making a piece a king through ```_king(self, piece)``` should be moved from the Checkers class to the Piece class. We removed the method from the Checkers class and created a new method ```set_king(self)``` within the piece class.
4. Moves in the game logic was originally represented as a tuple of two elements ```(pos, dest)``` with each element as a tuple storing coordinates on the board. To help keep track of jumping moves, we changed moves to a tuple of three elements ```(pos, dest, obj)``` with the third element as the object reference of the piece being jumped over during the move if it is a jumping move and None otherwise.
5. Added an ```is_valid_move(self, pos, dest)``` method for checking whether a given move is feasible instead of forcing users of the API to indirectly check through the ```piece_moves(self, pos)``` method.
6. Addressed design feedback that the ```add_piece(self, row, col, player)``` method of the Board class was missing a piece object parameter that would allow the user to pass in the piece object for storing on the board. We changed the method parameters to ```add_piece(self, pos, piece)``` with ```pos``` as tuple of row and column and ```player``` parameter removed as the player of the piece was accessible through the piece object itself.
7. Implemented design feedback recommending ```is_king``` attribute of the Piece class be made private. We also made all other attributes of Piece class private, and only accessible in restricted ways through public methods such as ```get_pos(self)```, ```set_pos(self, row, col)```, and ```is_king(self)```. This was done similarly with Board class.
8. Created new private method ```_check_winner(self)``` and private attributes ```_winner```, ```_game_over``` in Checkers class so that the logic calls on the method to check for a winner after every move and if a winner exists, the game is over.
9. Added new public method ```resign(self)``` that allows players to resign during their turn and hence end the game.
10. Added new public method ```draw(self)``` that allows players to request and agree to draws. Both players must call the method during their respective turn in order for a draw to occur.
11. Added new public method ```get_turn(self)``` to allow users of API to retrieve the turn player's Enum class.
12. Separated ```piece_moves(self, piece)``` into public facing ```piece_moves(self, pos)``` and internal private facing ```_all_piece_moves(self, pos)```. The public facing method will give a list of valid moves available for a turn player's piece, while the private facing method will give all possible moves (jump and non-jump) regardless of player turn for any piece and is used internally by code in ```player_moves(self)``` to aggregate and filter out the valid moves available from the current player's pieces.
13. The method ```_change_turns(self)``` was found redundant and removed because turn changing was implemented inside ```move(self, pos, dest)```. Similarly, ```_jump(self, piece, dest)``` was removed as jumping was coordinated inside ```move(self, pos, dest)```.
14. Added new public method ```get_game_state(self)``` that allows users of API to access private attributes for game states stored in ```self._game_over``` and ```self._winner```.

#### Milestone 2
1. Initially the implementation for consecutive jumps was to only allow players to choose the destinations of the piece after all possible full jumping moves have been exhausted. However this was deemed not user friendly and overly complicated and we instead chose to allow players to choose one jump at a time, even if this means allowing the same player to call ```move(self, pos, dest)``` multiple times during their turn.
2. In a multiple-jump move, a player must exhaust all possible jump moves for a piece before ending their turn. We fixed bug where during a multiple-jump move the player was allowed to choose a different piece if that piece could jump.
3. Added condition in ```move(self, pos, dest)``` that would end the current player's turn once the moving piece was kinged, and would not allow further moves in the case of consecutive jumps.
4. Fixed inequality signs in ```_all_piece_moves(self, pos)``` that led to indexing errors when trying to access pieces on the Board object.
5. Changed ```board_state(self)``` to dunder method ```__str__(self)```.
6. Changed implementation of checking winning states in ```_check_winner(self)``` by keeping track of moves since last capture for each player. If no pieces have been removed from the board during a player's previous 40 moves, the game ends in an automatic draw.
7. Draw proposal and acceptance mechanism changed so that when a player proposes a draw, the opponent can only accept a draw during the following turn, otherwise the draw offer is rescinded and reset. Thus, a player rejects a draw by not calling ```draw(self)``` after a proposal has been made.

## Developments since Milestones 2 for ```tui.py```
#### Milestone 2
We have integrated a click option for the board size which was at first defaulted to be a board of size 3. This can now be manipulated from the command line and left blank. Resign and draw functionality has also been added within the TUI to support not only player v players but also bot v player scenarios. Retrieving a move has also been split into two helper ```get_a_piece``` which takes a tuple of column and row (both indexed zero) and ensures that the selected piece belongs to the corresponding turn player and selecting it. This is also where players can make their first requests for a draw or a resign. This piece gets passed on to ```print_pick_moves``` where players are shown highlighted moves and asked to select a move. This all becomes integrated in the ```player_checkers``` function. We also made sure to highlight kinged pieces with a capital letter of their corresponding color (i.e. 'R' or 'B'). 
## Developments since Milestones 2 for ```gui.py```
#### Milestone 2
Jumping is added. When only jumping is available, it now shows through the orange color block. Resign and draw functionality has also been added through buttons on the right to support player v player and bot v player scenarios.
Kinging is added. We made sure to highlight kinged pieces through the king icon.
## Developments since Milestones 2 for ```bot.py```
#### Milestone 2
1. Initially, the bot file could not be run. This was addressed by fully implementing and debugging ```checkers.py``` to ensure that the game could be run.
2. The smart-bot originally used a strategy of taking the longest jumping move if possible and choosing a move at random if not. This was abandoned for a minimax algorithm approach since this algorithm yielded much better results.
3. More return possibilites were added to ```suggest_move(self)``` to address situations where the opponent requests a draw.
