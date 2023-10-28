import random
from enum import Enum


class Player(Enum):
    TOP = 0
    BOTTOM = 1


class Checkers:
    """
    Class for representing the systems interface for a game of Checkers, that
    allows players to make moves according to game logic on a virtual game 
    board
    """

    def __init__(self, n):
        """
        Constructor 

        Parameters:
            n: int: the number of rows of pieces a player starts with 
            to begin the game
        """
        # private attributes
        self. _n = n
        self._board = Board(2 * n + 2, 2 * n + 2)
        self.new_game()

    def new_game(self):
        """
        Resets the game to start state.

        Parameters:
            None

        Returns: 
            None
        """
        t = Player(random.randint(0, 1))
        self._turn = t
        self._p1 = set()
        self._p2 = set()
        self._game_over = False
        self._draw_p1 = False
        self._draw_p2 = False
        self._last_capture_p1 = 0
        self._last_capture_p2 = 0
        self._multjump = []
        self._winner = None
        self.start_turn = t

        n = self._n
        start = 1
        for i in range(0, n):
            for j in range(0, self._board.width()):
                if 2 * j + start < self._board.width():
                    piece = Piece(i, 2 * j + start, Player.TOP)
                    self._p1.add(piece)
                    self._board.add_piece((i, 2 * j + start), piece)
            start = (start + 1) % 2

        start = (n + 1) % 2
        for i in range(n, n + 2):
            for j in range(0, self._board.width()):
                if 2 * j + start < self._board.width():
                    self._board.remove((i, 2 * j + start))
            start = (start + 1) % 2

        start = (n + 1) % 2
        for i in range(n + 2, 2 * n + 2):
            for j in range(0, self._board.width()):
                if 2 * j + start < self._board.width():
                    piece = Piece(i, 2 * j + start, Player.BOTTOM)
                    self._p2.add(piece)
                    self._board.add_piece((i, 2 * j + start), piece)
            start = (start + 1) % 2

    def __str__(self):
        """
        Returns string representation of board state, with b indicating black 
        piece and r indicating red piece, with king pieces capitalized. 
        (Purpose of this method is mainly for debugging.)

        Parameters:
            None

        Returns: 
            None
        """
        image = ""
        for i in range(self._board.height()):
            for j in range(self._board.width()):
                piece = self._board.get((i, j))
                if piece is None:
                    image += "|_"
                else:
                    if self.start_turn == Player.BOTTOM:
                        if piece.get_player() == Player.TOP:
                            if piece.is_king():
                                image += "|R"
                            else:
                                image += "|r"
                        else:
                            if piece.is_king():
                                image += "|B"
                            else:
                                image += "|b"
                    else:
                        if piece.get_player() == Player.TOP:
                            if piece.is_king():
                                image += "|B"
                            else:
                                image += "|b"
                        else:
                            if piece.is_king():
                                image += "|R"
                            else:
                                image += "|r"

                if j == self._board.width() - 1:
                    image += "|\n"

        return image

    def resign(self):
        """
        Withdraws the current player from the game and ends the game.

        Parameters:
            None

        Returns: 
            None
        """
        self._game_over = True
        self._winner = Player((self._turn.value + 1) % 2)

    def draw(self):
        """
        Player requests for a draw. Draw can be made when both players call for
        a draw during their respective turns.

        Parameters:
            None

        Returns: 
            None
        """
        if self._turn == Player.TOP:
            self._draw_p1 = True
        else:
            self._draw_p2 = True

        if self._draw_p1 and self._draw_p2:
            self._game_over = True

    def get_game_state(self):
        """
        Returns the current game state: whether game is over, and the winner if
        the game is over.

        Parameters:
            None

        Returns: 
            Tuple(Boolean, Player): first element indicates game over and second
            element stores player object if winner exists
        """
        return (self._game_over, self._winner)

    def winner(self):
        """
        Prints the current game state: win, draw, or still in progress.

        Parameters:
            None

        Returns: 
            None
        """
        if self._winner is not None:
            print("Player", (self._winner.value + 1) % 2 + 1, "Loses.")
            print("Player", self._winner.value + 1, "Wins.")
        elif self._game_over:
            print("Draw has been made.")
        else:
            print('Game still in progress. No winner has been decided yet.')

    def _check_winner(self):
        """
        Internally evaluates current game state and assigns winner if one
        exists.

        Parameters:
            None

        Returns: 
            None
        """
        if len(self.player_moves()) == 0:
            self._game_over = True
            self._winner = Player((self._turn.value + 1) % 2)
        else:
            # automatic draw if 40 moves since last capture
            if self._turn == Player.TOP:
                if self._last_capture_p1 >= 40:
                    self._game_over = True
            else:
                if self._last_capture_p2 >= 40:
                    self._game_over = True

    def get_turn(self):
        """
        Gets the player of the current turn.

        Parameters:
            None

        Returns: 
            Player object of whose turn it is
        """
        return self._turn

    def set_turn(self, player):
        '''
        Assign the turn to a specified player.

        Parameters:
            player: Player: enum of player who we want to change the turn to

        Returns:
            None
        '''
        if not isinstance(player, Player):
            raise Exception('Must provide Player object')
        self._turn = player

    def player_moves(self):
        """
        Returns list of moves available to the player in the corresponding turn.
        If a jump is available, only jumps are shown.

        Parameters:
            player: Enum: top or bottom player

        Returns: List[moves]: list with each element containing the piece and
            the destination of the piece once the move is made
        """
        if len(self._multjump) > 0:
            return self._multjump

        if self._turn == Player.TOP:
            player_pieces = self._p1
        else:
            player_pieces = self._p2

        jumps = []
        non_jumps = []
        for piece in player_pieces:
            pos = piece.get_pos()
            for move in self._all_piece_moves(pos):
                if move[2] is not None:
                    jumps.append(move)
                else:
                    if len(jumps) == 0:
                        non_jumps.append(move)

        return jumps if len(jumps) > 0 else non_jumps

    def piece_moves(self, pos):
        """
        Returns list of valid moves available to a piece of the turn player
        on the board in the context of the game.

        Parameters:
            pos: Tuple(int): tuple of row and column of piece

        Returns: List[moves]: list with first element as tuple representing
            the position of the piece to be moved and the second element as the 
            tuple representing the destination of the piece once the move is 
            made, and the third element as a piece object that is jumped over
        """
        moves = []
        for move in self.player_moves():
            if move[0] == pos:
                moves.append(move)
        return moves

    def _all_piece_moves(self, pos):
        """
        Returns list of all jump and non-jump moves available to a specific 
        piece on the board regardless of game state, only to be used by
        internal logic.

        Parameters:
            pos: Tuple(int): tuple of row and column of piece

        Returns: List[moves]: list with first element as tuple representing
            the position of the piece to be moved and the second element as the 
            tuple representing the destination of the piece once the move is 
            made, and the third element as a piece object that is jumped over
        """
        i, j = pos
        piece = self._board.get((i, j))
        moves = []
        if piece is None:
            return []

        if piece.is_king():
            if i > 0:
                # NW
                if j > 0:
                    if self._board.get((i - 1, j - 1)) is None:
                        # regular move
                        moves.append((pos, (i - 1, j - 1), None))
                    else:
                        # check for possible jump move
                        if (i > 1 and j > 1 and
                            self._board.get((i - 1, j - 1)).get_player()
                            != piece.get_player()
                                and self._board.get((i - 2, j - 2)) is None):
                            # store jumped over piece in moves
                            moves.append((pos, (i - 2, j - 2),
                                          self._board.get((i - 1, j - 1))))

                # NE
                if j < 2 * self._n + 1:
                    if self._board.get((i - 1, j + 1)) is None:
                        moves.append((pos, (i - 1, j + 1), None))
                    else:
                        if (i > 1 and j < 2 * self._n and
                            self._board.get((i - 1, j + 1)).get_player()
                            != piece.get_player()
                                and self._board.get((i - 2, j + 2)) is None):
                            moves.append((pos, (i - 2, j + 2),
                                          self._board.get((i - 1, j + 1))))

            if i < 2 * self._n + 1:
                # SW
                if j > 0:
                    if self._board.get((i + 1, j - 1)) is None:
                        moves.append((pos, (i + 1, j - 1), None))
                    else:
                        if (i < 2 * self._n and j > 1 and
                            self._board.get((i + 1, j - 1)).get_player()
                            != piece.get_player()
                                and self._board.get((i + 2, j - 2)) is None):
                            moves.append((pos, (i + 2, j - 2),
                                          self._board.get((i + 1, j - 1))))
                # SE
                if j < 2 * self._n + 1:
                    if self._board.get((i + 1, j + 1)) is None:
                        moves.append((pos, (i + 1, j + 1), None))
                    else:
                        if (i < 2 * self._n and j < 2 * self._n and
                            self._board.get((i + 1, j + 1)).get_player()
                            != piece.get_player()
                                and self._board.get((i + 2, j + 2)) is None):
                            moves.append((pos, (i + 2, j + 2),
                                          self._board.get((i + 1, j + 1))))
        else:
            # only look in direction of player
            if piece.get_player() == Player.TOP:
                if i < 2 * self._n + 1:
                    # SW
                    if j > 0:
                        if self._board.get((i + 1, j - 1)) is None:
                            moves.append((pos, (i + 1, j - 1), None))
                        else:
                            if (i < 2 * self._n and j > 1 and
                                (self._board.get((i + 1, j - 1)).get_player()
                                 != piece.get_player())
                                    and self._board.get((i + 2, j - 2)) is None):
                                moves.append((pos, (i + 2, j - 2),
                                              self._board.get((i + 1, j - 1))))
                    # SE
                    if j < 2 * self._n + 1:
                        if self._board.get((i + 1, j + 1)) is None:
                            moves.append((pos, (i + 1, j + 1), None))
                        else:
                            if (i < 2 * self._n and j < 2 * self._n and
                                (self._board.get((i + 1, j + 1)).get_player()
                                 != piece.get_player())
                                    and self._board.get((i + 2, j + 2)) is None):
                                moves.append((pos, (i + 2, j + 2),
                                              self._board.get((i + 1, j + 1))))
            else:
                if i > 0:
                    # NW
                    if j > 0:
                        if self._board.get((i - 1, j - 1)) is None:
                            moves.append((pos, (i - 1, j - 1), None))
                        else:
                            if (i > 1 and j > 1 and
                                (self._board.get((i - 1, j - 1)).get_player()
                                 != piece.get_player())
                                    and self._board.get((i - 2, j - 2)) is None):
                                moves.append((pos, (i - 2, j - 2),
                                              self._board.get((i - 1, j - 1))))

                    # NE
                    if j < 2 * self._n + 1:
                        if self._board.get((i - 1, j + 1)) is None:
                            moves.append((pos, (i - 1, j + 1), None))
                        else:
                            if (i > 1 and j < 2 * self._n and
                                (self._board.get((i - 1, j + 1)).get_player()
                                 != piece.get_player())
                                    and self._board.get((i - 2, j + 2)) is None):
                                moves.append((pos, (i - 2, j + 2),
                                              self._board.get((i - 1, j + 1))))

        return moves

    def is_valid_move(self, pos, dest):
        """
        Returns whether move is valid for piece located at the specified 
        position. Player must have the current turn otherwise the move will
        be considered invalid.

        Parameters:
            pos: Tuple(int): tuple of row and column of piece
            dest: Tuple(int): tuple of row and column of destination of move

        Returns:
            Boolean: whether or not the move is valid
        """
        piece = self._board.get(pos)
        if piece is None or self._turn != piece.get_player():
            return False

        for move in self.player_moves():
            if move[0] == pos and move[1] == dest:
                return True

        return False

    def move(self, pos, dest):
        """
        Select a valid move on the board for the player in the current turn and
        update the location of the moved piece. (You actually move it)

        Parameters:
            pos: Tuple(int): tuple of row and column of piece
            dest: Tuple(int): tuple of row and column of destination of move

        Returns:
            None
        """
        if self._game_over:
            return

        piece = self._board.get((pos[0], pos[1]))
        if piece is not None and piece.get_player() == self._turn:
            # check if it is a valid move
            # print(pos[0], pos[1])
            found_move = None
            for move in self.player_moves():
                if move[0] == pos and move[1] == dest:
                    found_move = move
                    break

            if found_move is not None:
                # kings a piece if end of board reached by non-king piece
                kinged = False
                if not piece.is_king():
                    if self._turn == Player.TOP and dest[0] == 2 * self._n + 1:
                        piece.set_king()
                        kinged = True

                    if self._turn == Player.BOTTOM and dest[0] == 0:
                        piece.set_king()
                        kinged = True

                # coordinate removing of jumped pieces
                if found_move[2] is not None:
                    self._board.move(pos, dest)
                    piece.set_pos(dest[0], dest[1])

                    # remove jumped over piece
                    self._board.remove(move[2].get_pos())
                    if self._turn == Player.TOP:
                        self._p2.remove(move[2])
                    else:
                        self._p1.remove(move[2])

                    # change turns or continuing jumping
                    consecutive_jumps = []
                    for move in self._all_piece_moves(dest):
                        if move[2] is not None:
                            # can jump again!
                            consecutive_jumps.append(move)

                    # kinging ends turn (must also reset multjumps)
                    if len(consecutive_jumps) > 0 and not kinged:
                        self._multjump = consecutive_jumps
                    else:
                        self._multjump = []

                        if self._turn == Player.TOP:
                            self._last_capture_p1 = 0
                            self._draw_p2 = False
                        else:
                            self._last_capture_p2 = 0
                            self._draw_p1 = False
                        self._turn = Player((self._turn.value + 1) % 2)
                        self._check_winner()

                else:
                    self._board.move(pos, dest)
                    piece.set_pos(dest[0], dest[1])

                    # change turns and evaluate game state!
                    if self._turn == Player.TOP:
                        self._last_capture_p1 += 1
                        self._draw_p2 = False
                    else:
                        self._last_capture_p2 += 1
                        self._draw_p1 = False
                    self._turn = Player((self._turn.value + 1) % 2)
                    self._check_winner()

    def to_piece_grid(self):
        """
        Returns a copy of the state of the board as list of lists, with
        information on the locations and states of the players pieces.

        Parameters:
            None

        Returns:
            List[List]: list of lists
        """
        grid_list = [[] for _ in range(self._board.height())]
        for i in range(self._board.height()):
            for j in range(self._board.width()):
                piece = self._board.get((i, j))
                if piece is None:
                    grid_list[i] += ' '
                else:
                    if self.start_turn == Player.BOTTOM:
                        if piece.get_player() == Player.TOP:
                            if piece.is_king():
                                grid_list[i] += 'R'
                            else:
                                grid_list[i] += "r"
                        else:
                            if piece.is_king():
                                grid_list[i] += "B"
                            else:
                                grid_list[i] += "b"
                    else:
                        if piece.get_player() == Player.TOP:
                            if piece.is_king():
                                grid_list[i] += "B"
                            else:
                                grid_list[i] += "b"
                        else:
                            if piece.is_king():
                                grid_list[i] += 'R'
                            else:
                                grid_list[i] += "r"
        return grid_list


class Board:
    """
    Class for representing a generic n by n game board, with height and width n
    """

    def __init__(self, n, m):
        """
        Constructor

        Parameters:
            n: int: specifies the height of the board
            m: int: specifies the width of the board
        """
        self._height = n
        self._width = m
        self._cells = [[None for _ in range(m)] for _ in range(n)]

    def height(self):
        """
        Returns height of the board.

        Parameters:
            None

        Returns:
            int: height
        """
        return self._height

    def width(self):
        """
        Returns width of the board.

        Parameters:
            None

        Returns:
            int: width
        """
        return self._width

    def move(self, pos, dest):
        """
        Moves object in specified cell to a destination cell.

        Parameters:
            pos: Tuple(int): tuple of row and column of element to be moved
            dest: Tuple(int): tuple of row and column of destination

        Returns:
            None
        """
        if (0 <= pos[0] < self._height and 0 <= pos[1] < self._width and
                0 <= dest[0] < self._height and 0 <= dest[1] < self._width):
            self._cells[dest[0]][dest[1]] = self._cells[pos[0]][pos[1]]
            self._cells[pos[0]][pos[1]] = None
        else:
            raise Exception('Index out of bounds')

    def remove(self, pos):
        """
        Removes an object at the specified position on the board.

        Parameters:
            pos: Tuple(int): tuple of row and column of element to remove

        Returns:
            None
        """
        if 0 <= pos[0] < self._height and 0 <= pos[1] < self._width:
            self._cells[pos[0]][pos[1]] = None
        else:
            raise Exception('Index out of bounds')

    def get(self, pos):
        """
        Retrieve object at location on the board.

        Parameters:
            pos: Tuple(int): tuple of row and column of element to retrieve

        Returns:
            Object: element on the board
        """
        # check if positions are within boundaries
        if pos[0] == None or pos[1] == None:
            return None
        elif 0 <= pos[0] < self._height and 0 <= pos[1] < self._width:
            return self._cells[pos[0]][pos[1]]
        else:
            raise Exception('Index out of bounds')

    def add_piece(self, pos, piece):
        """
        Adds a piece to the board on a cell (specified by row and 
        column number).

        Parameters:
            pos: Tuple(int): tuple of row and column of location on board
            piece: Piece: piece object

        Returns:
            None
        """
        if 0 <= pos[0] < self._height and 0 <= pos[1] < self._width:
            self._cells[pos[0]][pos[1]] = piece
        else:
            raise Exception('Index out of bounds')

    def __str__(self):
        """
        Allows string visualization of pieces on the board for debugging.

        Parameters:
            None

        Returns:
            String
        """
        image = ""
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if cell is None:
                    image += " X "
                else:
                    image += " O "

                if j == len(row) - 1:
                    image += "\n"

        return image


class Piece:
    """
    Class for representing a checkers piece
    """

    def __init__(self, row, col, player):
        """
        Constructor

        Parameters:
            row: int: row index of piece on board
            col: int: column index of piece on board
            player: 0 or 1: indicating which player the piece belongs to
        """
        self._is_king = False
        self._row = row
        self._col = col
        self._player = player

    def get_pos(self):
        """
        Returns row and column of piece.

        Parameters:
            None

        Returns: 
            Tuple(int): row and column coordinate
        """
        return (self._row, self._col)

    def set_pos(self, row, col):
        """
        Sets row and column values of piece.

        Parameters:
            row: int: row coordinate
            col: int: column coordinate

        Returns: 
            None
        """
        self._row = row
        self._col = col

    def is_king(self):
        """
        Checks whether a piece is a king.

        Parameters:
            None

        Returns: 
            Boolean
        """
        return self._is_king

    def set_king(self):
        """
        Kings a piece.

        Parameters:
            None

        Returns: 
            None
        """
        self._is_king = True

    def get_player(self):
        """
        Returns player of the piece.

        Parameters:
            None

        Returns: 
            Player: owner of the piece
        """
        return self._player
