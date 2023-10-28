"""
Classes for implementing Checkers.

Examples:
    1) Creating a checkers board
        g1 = Checkers(3)

    2) Checking whether a given move is feasible for the turn player
        g1.is_valid_move((1,3), (3,4))

    3) Obtaining all valid moves of a piece for the turn player
        g1.piece_moves((1,4))

    4) Obtaining a list of all possible moves a turn player can make
        g1.player_moves()

    5) Checking if there is a winner / who the winner is
        g1.winner()
"""
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
        self._n = n
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
        raise NotImplementedError

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
        raise NotImplementedError

    def resign(self):
        """
        Withdraws the current player from the game and ends the game.

        Parameters:
            None

        Returns: 
            None
        """
        raise NotImplementedError

    def draw(self):
        """
        Player requests for a draw. Draw can be made when both players call for
        a draw during their respective turns.

        Parameters:
            None

        Returns: 
            None
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def winner(self):
        """
        Prints the current game state: win, draw, or still in progress.

        Parameters:
            None

        Returns: 
            None
        """
        raise NotImplementedError

    def _check_winner(self):
        """
        Internally evaluates current game state and assigns winner if one
        exists.

        Parameters:
            None

        Returns: 
            None
        """
        raise NotImplementedError

    def get_turn(self):
        """
        Gets the player of the current turn.

        Parameters:
            None

        Returns: 
            Player object of whose turn it is
        """
        raise NotImplementedError
    
    def set_turn(self, player: Player):
        '''
        Assign the turn to a specified player.

        Parameters:
            player: Player: enum of player who we want to change the turn to
        
        Returns:
            None
        '''
        raise NotImplementedError

    def player_moves(self):
        """
        Returns list of moves available to the player in the corresponding turn.
        If a jump is available, only jumps are shown.

        Parameters:
            player: Enum: top or bottom player

        Returns: List[moves]: list with each element containing the piece and
            the destination of the piece once the move is made
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def to_piece_grid(self):
        """
        Returns a copy of the state of the board as list of lists, with
        information on the locations and states of the players pieces.

        Parameters:
            None

        Returns:
            List[List]: list of lists
        """
        raise NotImplementedError


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
        raise NotImplementedError

    def width(self):
        """
        Returns width of the board.

        Parameters:
            None

        Returns:
            int: width
        """
        raise NotImplementedError

    def move(self, pos, dest):
        """
        Moves object in specified cell to a destination cell.

        Parameters:
            pos: Tuple(int): tuple of row and column of element to be moved
            dest: Tuple(int): tuple of row and column of destination

        Returns:
            None
        """
        raise NotImplementedError

    def remove(self, pos):
        """
        Removes an object at the specified position on the board.

        Parameters:
            pos: Tuple(int): tuple of row and column of element to remove

        Returns:
            None
        """
        raise NotImplementedError

    def get(self, pos):
        """
        Retrieve object at location on the board.

        Parameters:
            pos: Tuple(int): tuple of row and column of element to retrieve

        Returns:
            Object: element on the board
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def __str__(self):
        """
        Allows string visualization of pieces on the board for debugging.

        Parameters:
            None

        Returns:
            String
        """
        raise NotImplementedError


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
        raise NotImplementedError

    def set_pos(self, row, col):
        """
        Sets row and column values of piece.

        Parameters:
            row: int: row coordinate
            col: int: column coordinate

        Returns: 
            None
        """
        raise NotImplementedError

    def is_king(self):
        """
        Checks whether a piece is a king.

        Parameters:
            None

        Returns: 
            Boolean
        """
        raise NotImplementedError

    def set_king(self):
        """
        Kings a piece.

        Parameters:
            None

        Returns: 
            None
        """
        raise NotImplementedError

    def get_player(self):
        """
        Returns player of the piece.

        Parameters:
            None

        Returns: 
            Player: owner of the piece
        """
        raise NotImplementedError
