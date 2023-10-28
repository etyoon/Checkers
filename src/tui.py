import time

import click
from checkers import Board, Checkers, Player, Piece
from bot import RandomBot, SmartBot


class TUIPlayer:
    '''
    A simple class to store information about the TUI Player

    A TUI player can either a human player using the keyboard,
    or a bot.
    '''

    def __init__(self, n: int, player_type: str, board: Checkers,
                 player: Player, opponent: Player, bot_delay: float):
        '''
        Constructor

        Parameters:
        n: [int] the players number
        player_type: "human", "random-bot", or "smart-bot"
        board: The Checkers board of m size
        player: whether player is top or bottom
        opponent: whether opponent is top or bottom
        bot_delay: When playing as a bot, an artificial delay
           (in seconds) to wait before making a move.
        '''
        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        if player_type == "random-bot":
            self.name = f"Random Bot {n}"
            self.bot = RandomBot(board, player, opponent)
        elif player_type == "smart-bot":
            self.name = f"Smart Bot {n}"
            self.bot = SmartBot(board, player, opponent)
        self.board = board
        self.player = player
        self.bot_delay = bot_delay

    def get_a_piece(self, row=None, column=None) -> tuple:
        '''
        Helper function that obtains a piece via user input
        Checks to make sure it is a piece that can move and is owned
          by the player
        Also handels resign and draw situations

        Inputs: None
        row and column variable are default none and shouln't be changed

        Outputs: Tuple of row and column of selected piece
        '''
        while self.board._board.get((row, column)) == None:
            while row == None:
                print(self.player.name + ' what piece do you want to move?')
                r = input("Row: ")
                if r.lower() == 'resign':
                    self.board.resign()
                    return None
                elif r.lower() == 'draw':
                    self.board.draw()
                    return None
                elif not r.isdigit():
                    print('Please provide an integer row')
                elif int(r) in range(self.board._board.height()):
                    row = int(r)
                else:
                    print('The row provided is not on the board')
                    print('Please try again')
            print()
            while column == None:
                col = input("Column: ")
                if not col.isdigit():
                    print('Please provide an integer column')
                elif int(col) in range(self.board._board.width()):
                    piece = self.board._board.get((row, int(col)))
                    if piece == None:
                        print('That is not your piece or it is an empty space')
                        print('Please pick again')
                        row = None
                        column = None
                        break
                    elif len(self.board.piece_moves((piece._row, piece._col))) \
                            == 0:
                        print('That piece cannot move')
                        print('Please pick again')
                        row = None
                        column = None
                        break
                    else:
                        if piece.get_player() == self.player:
                            column = int(col)
                            return (row, column)
                else:
                    print('The column provided is not on the baord')
                    print('Please try again')

    def print_pick_moves(self, row: int, column: int, move_lst: list) -> tuple:
        '''
        Helper function that displays possible moves of selected piece to player
        Ensures that move is viable and also that players take any jumps
           available

        Inputs:
        row: [int] row of selected piece
        column: [int] column of selected piece
        move_lst: [list] list of all possible moves a player can make

        Outputs: Tuple of row and column of original placement of piece and row
           and column of the new destination of the piece
        '''
        while self.board.get_turn() == self.player:
            count = 0
            move_index = dict()
            print('Please choose a move:')
            index = -1
            while int(index) > len(move_lst) + 1 or int(index) < 0:
                count = 0
                for i, move in enumerate(move_lst):
                    if move[0] == (row, column):
                        count += 1
                        move_index[count] = i
                        print(count, ")", move[0], "->", move[1])
                index = input("> ")
                if int(index) > count or int(index) < 0:
                    print('Sorry that is not a choice')
                elif not index.isdigit():
                    print('Choice must be an integer')
                else:
                    return (move_lst[move_index[int(index)]][0],
                            move_lst[move_index[int(index)]][1])

    def get_move(self, players: dict):
        '''
        Combines get_a_piece and print_pick_moves to prompt player for a piece
           and where to move the piece
        If the player is a bot, ask the bot to suggest a move.

        Inputs: None

        Outputs: Either a tuple of row and column of original placement of piece 
           and row and column of the new destination of the piece
           or None if a draw has been requested
        '''
        if self.bot is not None:
            time.sleep(self.bot_delay)
            post_dest = self.bot.suggest_move()
            print(f"{self.name}> " + str(post_dest))
            return post_dest
        else:
            move_lst = self.board.player_moves()
            if move_lst[0][2] != None:
                jump_index = dict()
                print('A Jump is available and must be taken')
                count = 0
                for i, move in enumerate(move_lst):
                    count += 1
                    jump_index[count] = i
                    print(count, ")", move[0], "->", move[1])
                index = input("> ")
                if int(index) > len(move_lst) + 1 or int(index) < 0:
                    print('That is not a valid move')
                else:
                    return (move_lst[jump_index[int(index)]][0],
                            move_lst[jump_index[int(index)]][1])
            else:
                pd = self.get_a_piece()
                if self.board._draw_p1 or self.board._draw_p2:
                    self.board.set_turn(Player(
                                        (self.board.get_turn().value + 1) % 2))
                    for value in players.values():
                        if value.bot is not None:
                                return None
                    print("Opponent has requested a draw.")
                    print('Would you like to draw')
                    y_n = input('Y/N?')
                    if y_n.lower() == 'y':
                        self.board.draw()
                        return None
                    else:
                        self.board.set_turn(Player(
                            (self.board.get_turn().value + 1) % 2))
                        self.board._draw_p1 = False
                        self.board._draw_p2 = False
                elif pd != None:
                    return(self.print_pick_moves(pd[0], pd[1], move_lst))


def print_board(board: Checkers) -> None:
    '''
    Prints the board to the screen

    Input: [Checkers] board to print

    Returns: None
    '''
    print(board)


def play_checkers(board: Checkers, players: dict) -> None:
    '''
    Plays a game of checkers on the terminal

    Inputs:      
    board: [Checkers] board to play on
    players: [Dictionary] maps TOP or BOTTOM to TUIPlayer objects.

    Outputs: None
    '''
    while not board._game_over:
        current = players[board.get_turn()]

        print()
        print_board(board)
        print()

        p_d_loc = current.get_move(players)

        if p_d_loc == ['Y', 'Y']:
            board.draw()
        elif p_d_loc == ['N', 'N']:
            board.set_turn(Player((board.get_turn().value + 1) % 2))
            print('The bot has rejected your draw request')
        elif p_d_loc != None:
            board.move(p_d_loc[0], p_d_loc[1])

    print()
    print_board(board)
    print(board.winner())


@click.command(name="checkers-tui")
@click.option('--board-size',
            type=click.INT, default = 3)
@click.option('--player1',
              type=click.Choice(['human', 'random-bot', 'smart-bot'],
                                case_sensitive=False),
              default="human")
@click.option('--player2',
              type=click.Choice(['human', 'random-bot', 'smart-bot'],
                                case_sensitive=False),
              default="human")
@click.option('--bot-delay', type=click.FLOAT, default=0.5)

def cmd(player1, player2, bot_delay, board_size):
    board = Checkers(board_size)
    player1 = TUIPlayer(1, player1, board, Player.TOP, Player.BOTTOM, bot_delay)
    player2 = TUIPlayer(2, player2, board, Player.BOTTOM, Player.TOP, bot_delay)

    players = {Player.TOP: player1, Player.BOTTOM: player2}

    play_checkers(board, players)


if __name__ == "__main__":
    cmd()
