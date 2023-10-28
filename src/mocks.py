"""
Stub and mock implementations of the Checkers class
"""
from checkers import Player
import random


class CheckersStub:
    """
    Stub implementation of the Checkers class
    """

    def __init__(self, n):
        pass

    def new_game(self) -> None:
        pass

    def board_state(self) -> None:
        pass

    def resign(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def winner(self) -> None:
        pass

    def _check_winner(self) -> None:
        pass

    def get_turn(self):
        return Player.TOP

    def player_moves(self) -> list:
        return []

    def _piece_moves(self, pos) -> list:
        return []

    def is_valid_move(self, pos, dest) -> bool:
        return True

    def move(self, pos, dest) -> None:
        pass

    def to_piece_grid(self) -> list:
        return []

    def is_bottled(selff, piece) -> bool:
        return True

    def _ghost_piece_jumps(self, pos, piece) -> list:
        return []

    def jump_sequences(self, pos, piece) -> list:
        return []

    def _has_last_move(self, player) -> bool:
        return False


class BoardStub:
    """
    Stub implementation of the BoardStub
    """

    def __init__(self, n, m):
        pass

    def height(self) -> int:
        return 1

    def width(self) -> int:
        return 1

    def move(self, pos, dest) -> None:
        pass

    def remove(self, pos) -> None:
        pass

    def get(self, pos):
        return None

    def add_piece(self, row, col, player) -> None:
        pass

    def __str__(self) -> str:
        return "BOARD"


class PieceStub:
    def __init__(self, row, col, player):
        pass

    def get_pos(self) -> tuple:
        return (0, 0)

    def set_pos(self, row, col) -> None:
        pass

    def is_king(self) -> bool:
        return False

    def set_king(self) -> None:
        pass

    def get_player(self) -> Player:
        return Player.TOP


class CheckersMock:
    """
    Mock implementation of the Checkers class

    Expected behaviours:
    - Stores the full board internally, but we only ever
      modify the first row of the player. 
    - Only allows simple moves
    """

    def __init__(self, n):
        self._n = n
        self._board = BoardMock(2 * n + 2, 2 * n + 2)
        self.new_game()

    def new_game(self) -> None:
        self._turn = Player(random.randint(0, 1))
        self._p1 = set()
        self._p2 = set()
        self._game_over = False
        self._winner = None
        for col_num in range(1, self._n * 2 + 2, 2):
            piece = PieceMock(0, col_num, Player.TOP)
            self._p1.add(piece)
            self._board.cells[0][col_num] = piece
        for col_num in range(0, self._n * 2 + 2, 2):
            piece = PieceMock(len(self._board.cells)-1, col_num, Player.BOTTOM)
            self._p2.add(piece)
            self._board.cells[-1][col_num] = piece

    def board_state(self) -> None:
        image = ""
        for i, row in enumerate(self._board.cells):
            for j, piece in enumerate(row):
                if piece is None:
                    image += "|_|"
                else:
                    if piece.player == Player.TOP:
                        if piece.is_king():
                            image += "|R|"
                        else:
                            image += "|r|"
                    else:
                        if piece.is_king():
                            image += "|B|"
                        else:
                            image += "|b|"

                if j == len(row) - 1:
                    image += "\n"

        print(image)

    def winner(self) -> None:
        if self._winner is not None:
            print("Player", (self._winner.value + 1) % 2 + 1, "Loses.")
            print("Player", self._winner.value + 1, "Wins.")
        elif self._game_over:
            print("Draw.")
        else:
            print('No winner has been decided yet.')

    def _check_winner(self) -> None:
        if len(self.player_moves()) == 0:
            self._game_over = True
            self._winner = Player(self._turn.value + 1 % 2)

    def get_turn(self):
        return self._turn

    def player_moves(self) -> list:
        moves = []
        if self._turn == Player.TOP:
            for piece in self._p1:
                pos = (piece.row, piece.col)
                moves.extend([(piece, dest)
                             for dest in self._piece_moves(pos)])
        else:
            for piece in self._p2:
                pos = (piece.row, piece.col)
                moves.extend([(piece, dest)
                             for dest in self._piece_moves(pos)])
        return moves

    def _piece_moves(self, pos) -> list:
        # only simple moves for now?
        i, j = pos
        piece = self._board.cells[i][j]
        moves = []
        if piece.is_king():
            if i > 0:
                if j > 0:
                    if self._board.cells[i-1][j-1] is None:
                        moves.append(((i, j), (i-1, j-1)))
                if j < 2 * self._n + 1:
                    if self._board.cells[i-1][j+1] is None:
                        moves.append(((i, j), (i-1, j+1)))
            if i < 2 * self._n + 1:
                if j > 0:
                    if self._board.cells[i+1][j-1] is None:
                        moves.append(((i, j), (i+1, j-1)))
                if j < 2 + self._n + 1:
                    if self._board.cells[i+1][j+1] is None:
                        moves.append(((i, j), (i+1, j+1)))
        else:
            if piece.player == Player.TOP:
                if j > 0:
                    if self._board.cells[i+1][j-1] is None:
                        moves.append(((i, j), (i+1, j-1)))
                if j < 2 + self._n + 1:
                    if self._board.cells[i+1][j+1] is None:
                        moves.append(((i, j), (i+1, j+1)))
            else:
                if j > 0:
                    if self._board.cells[i-1][j-1] is None:
                        moves.append(((i, j), (i-1, j-1)))
                if j < 2 * self._n + 1:
                    if self._board.cells[i-1][j+1] is None:
                        moves.append(((i, j), (i-1, j+1)))
        return moves

    def is_valid_move(self, pos, dest) -> bool:
        piece = self._board.get(pos)
        if piece is None or self._turn != piece.get_player():
            return False

        for move in self.player_moves():
            if move[0] == pos and move[1] == dest:
                return True

        return False

    def move(self) -> None:
        if self._game_over:
            print('Game is over.')
            return

        # check first if piece belongs to player in corresponding turn
        piece = self._board.get((pos[0], pos[1]))
        # print(piece)
        if piece is not None and piece.get_player() == self._turn:
            # check if it is a valid move
            found_move = None
            for move in self.player_moves():
                if move[0] == pos and move[1] == dest:
                    found_move = move
                    break

            if found_move is None:
                raise Exception("Invalid move.")
            else:
                # kings a piece if end of board reached by non-king piece
                if not piece.is_king():
                    if (piece.get_player() == Player.TOP and
                            dest[0] == 2 * self._n + 1):
                        piece.set_king()

                    if piece.get_player() == Player.BOTTOM and dest[0] == 0:
                        piece.set_king()
                    # change turns?
                    self._turn = Player((self._turn.value + 1) % 2)
                    self._check_winner()
                else:
                    self._board.move(pos, dest)
                    piece.set_pos(dest[0], dest[1])

                    # change turns - evaluate game state!
                    self._turn = Player((self._turn.value + 1) % 2)
                    self._check_winner()
        else:
            raise Exception('Could not find piece of turn player.')

    def to_piece_grid(self):
        grid_list = [[] for _ in range(self._board.height())]
        for i in range(self._board.height()):
            for j in range(self._board.width()):
                piece = self._board.get((i, j))
                if piece is None:
                    grid_list[i] += ' '
                else:
                    if piece.get_player() == Player.TOP:
                        if piece.is_king():
                            grid_list[i] += "R"
                        else:
                            grid_list[i] += "r"
                    else:
                        if piece.is_king():
                            grid_list[i] += "B"
                        else:
                            grid_list[i] += "b"

        return grid_list

    def is_bottled(self, piece):
        return False

    def _has_last_move(self, player):
        return False


class BoardMock:
    """
    Mock implementation of the Board Class
    """

    def __init__(self, n, m):
        self._height = n
        self._width = m
        self.cells = [[None for _ in range(m)] for _ in range(n)]

    def height(self):
        return self._height

    def width(self):
        return self._width

    def move(self, pos, dest) -> None:
        if (0 <= pos[0] < self._height and 0 <= pos[1] < self._width and
                0 <= dest[0] < self._height and 0 <= dest[1] < self._width):
            self._cells[dest[0]][dest[1]] = self._cells[pos[0]][pos[1]]
            self._cells[pos[0]][pos[1]] = None
        else:
            raise Exception('Index out of bounds')

    def add_piece(self, row, col, player) -> None:
        pass

    def __str__(self) -> str:
        image = ""
        for i, row in enumerate(self.cells):
            for j, piece in enumerate(row):
                if piece is None:
                    image += "|_|"
                else:
                    if piece.player == Player["TOP"]:
                        if piece.is_king():
                            image += "|R|"
                        else:
                            image += "|r|"
                    else:
                        if piece.is_king():
                            image += "|B|"
                        else:
                            image += "|b|"

                if j == len(row) - 1:
                    image += "\n"

        return image

    def get(self, pos):
        if 0 <= pos[0] < self._height and 0 <= pos[1] < self._width:
            return self._cells[pos[0]][pos[1]]
        else:
            raise Exception('Index out of bounds')


class PieceMock:
    """
    Mock implementation of the Piece Class
    """

    def __init__(self, row, col, player):
        self._is_king = False
        self.row = row
        self.col = col
        self.player = player

    def get_pos(self):
        return (self._row, self._col)

    def set_pos(self, row, col):
        self._row = row
        self._col = col

    def is_king(self) -> bool:
        return self._is_king

    def set_king(self):
        self._is_king = True

    def get_player(self):
        return self._player
