from typing import Union, Dict
import sys
import os
import pygame
import click
import time
from checkers import Checkers, Player
from mocks import CheckersStub, CheckersMock
from bot import RandomBot, SmartBot

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

WIDTH = 700
HEIGHT = 700
BUTTON_WIDTH = 150
TEXT_SIZE = WIDTH // 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 191, 0)
SKY_BLUE = (99, 197, 218)
GREEN = (175, 225, 175)
COOLER_RED = (247, 67, 58)

# need to have docstrings


class Mouse:

    def __init__(self) -> None:

        self.intial_x = -1
        self.intial_y = -1
        self.x = 0
        self.y = 0


class GUIPlayer:
    """
    Simple class to store information about a GUI player
    A TUI player can either a human player using the keyboard,
    or a bot.
    """

    def __init__(self, n: int, player_type: str, board: Checkers, player: Player, opponent: Player):
        """
        Constructor
        Parameters:
        n: [int] the players number
        player_type: "human", "random-bot", or "smart-bot"
        board: The Checkers board of m size
        player: Whether player is top or bottom
        opponent: Whether opponent is top or bottom
        """
        self.board = board
        self.player = player

        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        if player_type == "random-bot":
            self.name = f"Random Bot {n}"
            self.bot = RandomBot(board, player, opponent)
        if player_type == "smart-bot":
            self.name = f"Smart Bot {n}"
            self.bot = SmartBot(board, player, opponent)


def calculate_pos(n, y: int, x: int):
    """
    Calculates what grid you are in

    Args:
        y: y coordinate
        x: x coordinate

    returns: location in form of tuple. (x, y)
    """
    rows, cols = 2*n + 2, 2*n + 2
    return (int((x / HEIGHT * rows)), int((y / WIDTH * cols)))


def draw_board(surface: pygame.surface.Surface, board: Checkers, mouse:
               Mouse) -> None:
    """
    Draws the board

    Args:
        surface: The surface to draw on
        board: The Checkers board of m size
        mouse: A boolean saying if the mouse is being pressed down or not

    Returns: None
    """
    grid = board.to_piece_grid()
    nrows = len(grid)
    ncols = len(grid[0])

    # Compute the row height and column width
    rh = HEIGHT // nrows + 1
    cw = WIDTH // ncols + 1

    # Draws the squares
    for i, r in enumerate(grid):
        for j, temp in enumerate(r):
            rect = (j * cw, i * rh, cw, rh)
            if (i + j) % 2 == 0:
                color = BLACK
            else:
                color = WHITE

            pygame.draw.rect(surface, color=color,
                             rect=rect)

    player_moves = board.player_moves()
    if len(player_moves) > 0 and player_moves[0][2] is not None:
        moves = [i[1] for i in player_moves]
        for move in moves:
            rect = (move[1] * cw, move[0] * rh, cw, rh)
            pygame.draw.rect(surface, color=ORANGE,
                             rect=rect)

    else:
        if mouse.intial_x != -1:
            board_pos = (mouse.intial_x, mouse.intial_y)
            move_grid = board.piece_moves(board_pos)
            moves = [i[1] for i in move_grid]
            for move in moves:
                rect = (move[1] * cw, move[0] * rh, cw, rh)
                pygame.draw.rect(surface, color=YELLOW,
                                 rect=rect)
    # Draw the pieces
    for i, r in enumerate(grid):
        for j, piece_color in enumerate(r):
            center = (j * cw + cw // 2, i * rh + rh // 2)
            radius = rh // 2 - 8
            if piece_color != ' ':
                # For king
                # photo source: www.pngwing.com/
                crown = pygame.transform.scale(pygame.image.load(
                    'crown.png'), (radius * 1.5, radius * 1.5))

                if piece_color == 'R':
                    color = RED
                    pygame.draw.circle(surface, color=color,
                                       center=center, radius=radius)
                    surface.blit(
                        crown, (center[0]-crown.get_width()//2, center[1]
                                - crown.get_height()//2))
                elif piece_color == 'B':
                    color = BLACK
                    pygame.draw.circle(surface, color=color,
                                       center=center, radius=radius)
                    surface.blit(
                        crown, (center[0]-crown.get_width()//2, center[1]
                                - crown.get_height()//2))
                # for regular piece
                elif piece_color == 'r':
                    color = RED
                    pygame.draw.circle(surface, color=color,
                                       center=center, radius=radius)
                elif piece_color == 'b':
                    color = BLACK
                    pygame.draw.circle(surface, color=color,
                                       center=center, radius=radius)


def draw_buttons(surface: pygame.surface.Surface, pos: list, draw:
                 bool) -> None:
    """
    Draws the buttons

    Inputs: 
    surface: The surface to draw on
    pos: The position of the mouse
    draw: Tells if the previous move was draw or not (if it was, drawing would
    end the game).

    Return: None
    """

    rect_size = (BUTTON_WIDTH, HEIGHT / 2)
    draw_color = RED
    quit_color = WHITE

    font = pygame.font.SysFont('Arial', TEXT_SIZE)
    # xtx update these text colors they are ass
    draw_text_color = WHITE
    quit_text_color = RED

    # First check if mouse is over a button
    if(pos[0] >= WIDTH):
        # Top box
        if(pos[1] < HEIGHT / 2):
            draw_color = SKY_BLUE
            draw_text_color = WHITE
        # Bottom button
        else:
            quit_color = SKY_BLUE
            quit_text_color = WHITE

    if draw == True:
        top_text = "Decline"
        bottom_text = "Accept"
    else:
        top_text = "Draw"
        bottom_text = "Quit"
    # Draws the draw rectangle
    corner = (WIDTH, 0)
    draw_rect = pygame.Rect(corner, rect_size)
    center = draw_rect.center
    pygame.draw.rect(surface, draw_color, draw_rect)
    draw_text = font.render(top_text, True, draw_text_color)
    text_rect = draw_text.get_rect(center=center)
    surface.blit(draw_text, text_rect)

    # Draws the quit button
    corner = (WIDTH, HEIGHT / 2)
    quit_rect = pygame.Rect(corner, rect_size)
    center = quit_rect.center
    pygame.draw.rect(surface, quit_color, quit_rect)
    quit_text = font.render(bottom_text, True, quit_text_color)
    text_rect = quit_text.get_rect(center=center)
    surface.blit(quit_text, text_rect)


def winner_screen(surface: pygame.surface.Surface, winner: str) -> None:
    """
    Displays the winner

    Inputs:
    surface: The surface to draw on
    winner: The winner

    Returns: None
    """
    center = [WIDTH // 2, HEIGHT // 2]
    rect_size = (WIDTH // 3, HEIGHT // 4)
    hundo_count = 8
    # emoji source: www.stickpng.com
    one_hundo = pygame.transform.scale(pygame.image.load(
        'hundred_emoji.png'), (WIDTH // hundo_count, HEIGHT //
                               hundo_count))

    for i in range(hundo_count):
        for j in range(hundo_count):
            surface.blit(one_hundo, (i * (WIDTH // hundo_count),
                         j * (HEIGHT // hundo_count)))

    rect = pygame.Rect(center, rect_size)
    rect.center = center
    pygame.draw.rect(surface, BLACK, rect)

    font = pygame.font.SysFont('Arial', TEXT_SIZE)
    top_text = font.render("{} won!".format(winner), True, WHITE)
    bottom_text = font.render("\(^-^)/", True, WHITE)
    text_rect = top_text.get_rect(center=center)
    surface.blit(top_text, text_rect)

    center[1] += TEXT_SIZE
    text_rect = bottom_text.get_rect(center=center)
    surface.blit(bottom_text, text_rect)


def play_checkers(board: Checkers, players: dict, bot_delay: float,
                  board_size: int) -> None:
    """
    Playes the checkers

    Parameters:
    board: The Checkers board of m size
    players: Whether player is top or bottom
    bot_delay: When playing as a bot, an artificial delay
           (in seconds) to wait before making a move.
    board_size: Board size to make the board.

    Returns: None
    """
    pygame.init()
    surface = pygame.display.set_mode((WIDTH + BUTTON_WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    mouse = Mouse()
    source = None
    destination = None
    draw = False
    while not board._game_over:
        # plays the game
        current = players[board.get_turn()]
        if board.get_turn() == Player.TOP:
            player = 'Player 1'
        else:
            player = 'Player 2'
        pygame.display.set_caption(
            "Checkers: Currently it's {}'s turn".format(player))

        events = pygame.event.get()
        for event in events:
            # To quit the program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            pos = pygame.mouse.get_pos()
            board_pos = calculate_pos(board_size, pos[0], pos[1])
            mouse.x = board_pos[0]
            mouse.y = board_pos[1]

            if current.bot is None:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if need to reset the intial position of the mouse
                    if mouse.intial_x == -1:
                        mouse.intial_x = board_pos[0]
                        mouse.intial_y = board_pos[1]

                    # Check if on a button
                    if(pos[0] > WIDTH):
                        if(pos[1] < HEIGHT / 2):
                            # If last player called for draw but if mouse is in
                            # this position it is same as declining so just swap
                            # the turns and set draw = False
                            if draw:
                                draw = False
                                board._draw_p1 = False
                                board._draw_p2 = False
                            # Otherwise this is first time calling a draw so
                            # call draw and set True
                            else:
                                board.draw()
                                draw = True
                            if board.get_turn() == Player.TOP:
                                board.set_turn(Player.BOTTOM)
                            else:
                                board.set_turn(Player.TOP)
                        else:
                            # Check if it is a 'yes' button or a 'Quit' button,
                            # if yes call draw, player = "Nobody" should set
                            # game over
                            if draw:
                                board.draw()
                            # Else user wanted to quit so just quit
                            else:
                                pygame.quit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if (pos[0] < WIDTH):
                        source = (mouse.intial_x, mouse.intial_y)
                        destination = (mouse.x, mouse.y)
                        if board.is_valid_move(source, destination):
                            board.move(source, destination)
                    mouse.intial_x = -1
                    mouse.intial_y = -1

        if current.bot is not None:
            pygame.time.wait(int(bot_delay * 1000))
            source, destination = current.bot.suggest_move()
            # This is the case when the player requests a draw and bot rejects
            if source == 'N':
                draw = False
                if board.get_turn() == Player.TOP:
                    board.set_turn(Player.BOTTOM)
                else:
                    board.set_turn(Player.TOP)
            elif source == 'Y':
                board.draw()
            else:
                board.move(source, destination)

        draw_board(surface, board, mouse)
        draw_buttons(surface, pos, draw)
        pygame.display.update()
        clock.tick(120)

    draw_board(surface, board, mouse)
    if board._winner is None:
        player = "Nobody"
    winner_screen(surface, player)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()


@ click.command(name="checkers-gui")
@ click.option('--board-size',
               type=click.INT, default=3)
@ click.option('--player1',
               type=click.Choice(['human', 'random-bot', 'smart-bot'],
                                 case_sensitive=False),
               default="human")
@ click.option('--player2',
               type=click.Choice(['human', 'random-bot', 'smart-bot'],
                                 case_sensitive=False),
               default="human")
@ click.option('--bot-delay', type=click.FLOAT, default=0)
def cmd(player1, player2, bot_delay, board_size):
    board = Checkers(board_size)
    player1 = GUIPlayer(1, player1, board, Player.TOP,
                        Player.BOTTOM)
    player2 = GUIPlayer(2, player2, board, Player.BOTTOM,
                        Player.TOP)

    players = {Player.TOP: player1, Player.BOTTOM: player2}

    play_checkers(board, players, bot_delay, board_size)


if __name__ == "__main__":
    cmd()
