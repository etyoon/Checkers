"""
Bots for Checkers
"""
import random
from checkers import Checkers, Player
from typing import Union
import click
import copy
import math

#
# BOTS
#


class RandomBot:
    """
    Simple Bot that just picks a move at random
    """

    def __init__(self, game, player, opponent):
        """
        Constructor

        Parameters:
          game: game of Checkers the bot will play
          player: bot's player identity
          opponent: opponent's player identity
        """
        self._game = game
        self._player = player
        self._opponent = opponent

    def suggest_move(self):
        """
        Suggests a move at random. If the opponent requests a draw, accepts at
        random.

        Returns: tuple of piece position tuple and destination position tuple
        """
        if self._game._draw_p1 or self._game._draw_p2:
            return random.choice([['Y', 'Y'], ['N', 'N']])
        move_chosen = random.choice(self._game.player_moves())
        curr_idx, dest_idx, _ = move_chosen

        return curr_idx, dest_idx


class SmartBot:
    # http://www.cs.columbia.edu/~devans/TIC/AB.html
    # source for alpha-beta pruning minimax psuedo-code:
    #       https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
    """
    Smart bot.

    Using an alpha-beta pruning method on a minimax algorithm, it will keep
    track of possible plays (until a player wins or up to depth of 5) that
    result from making certain moves. The last state of the board at each play
    is evaluated to determine how favorable the play is for the bot. The
    methodology for the evaluation is as follows (adapted from website cited
    above).
        - Who has more/better pieces? Kings are worth 5000, normal pieces are
        worth 3000.
        - Whose pieces are, on average, closer to being kings? The closeness of
        each non-king pieces are added (the higher the number, the clower the
        piece is to being a king). An average of this sum is multiplied by 10.
        - A total of these two categories are added for each player.
        - The opponent's evaluation score is subtracted from the bot's
        evaluation score to determine the evaluation number for the state of
        the board.
    Using this evaluation number, the algorithm will discard a possible play if
    there is a better play (more favorable for the bot) that has been explored.

    If the opponent requests a draw, rejects the request if bot has more pieces
    on the board.
    """
    def __init__(self, game, player, opponent):
        """
        Constructor

        Parameters:
          game: game of Checkers the bot will play
          player: bot's player identity
          opponent: opponent's player identity
        """
        self._game = game
        self._player = player
        self._opponent = opponent

    def suggest_move(self):
        """
        Suggests a move using an alpha-beta pruning minimax algorithm.

        Returns: tuple: tuple of current position of the piece to be moved and
                        the destination position
        """
        if self._game._draw_p1 or self._game._draw_p2:
            if self.evaluation(self._game) >= 3000:
                return ['N', 'N']
            else:
                return ['Y', 'Y']
        d, moves = self.abminimax(self._game, 5, -9999, 9999, True)
        chosen_move = random.choice(list(moves))
        return chosen_move[0], chosen_move[1]

    def abminimax(self, game, depth, alpha, beta, is_maximizing):
        """
        Alpha-beta pruning minimax algorithm.

        Parameters:
            game: Checkers: game of checkers to be played
            depth: int: the maximum depth to which the algorithm should keep
                        track of plays to
            alpha: int: number for alpha
            beta: int: number for beta
            is_maximizing: bool: whether the player that is currently in
                                    consideration wants to maximize the
                                    evaluation score of the board

        Returns: tuple: tuple of most favorable evaluation score for the
                        player currently in consideration and a list of the
                        initial move(s) that leads to that favored game state.
        """
        if depth == 0 or game._game_over:
            return self.evaluation(game), []
        if is_maximizing:
            maxEval = -math.inf
            best_moves = []
            for m in game.player_moves():
                curr_pos, dest, _ = m
                gamecopy = copy.deepcopy(game)
                gamecopy.move(curr_pos, dest)
                if gamecopy.get_turn() == self._player:
                    value = self.abminimax(
                        gamecopy, depth, alpha, beta, True)[0]
                else:
                    value = self.abminimax(
                        gamecopy, depth-1, alpha, beta, False)[0]
                maxEval = max(maxEval, value)
                if maxEval == value:
                    best_moves.append((curr_pos, dest))
                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    break
            return maxEval, best_moves
        else:
            minEval = math.inf
            best_moves = []
            for m in game.player_moves():
                curr_pos, dest, _ = m
                gamecopy = copy.deepcopy(game)
                gamecopy.move(curr_pos, dest)
                if gamecopy.get_turn() == self._opponent:
                    value = self.abminimax(
                        gamecopy, depth, alpha, beta, False)[0]
                else:
                    value = self.abminimax(
                        gamecopy, depth-1, alpha, beta, True)[0]
                minEval = min(minEval, value)
                if minEval == value:
                    best_moves.append((curr_pos, dest))
                beta = min(beta, minEval)
                if beta <= alpha:
                    break
            return minEval, best_moves

    def evaluation(self, game):
        """
        Evaluates the state of the game board using the methodology described in
        doc string for the SmartBot class.

        Parameters:
            game: Checkers: game to checkers to be evaluated

        Returns: int: evaluation score
        """
        bot_score = 0
        opp_score = 0
        bot_potential = 0
        opp_potential = 0
        if game._winner == self._player:
            return math.inf
        elif game._winner == self._opponent:
            return -math.inf
        else:
            if self._player == Player.TOP:
                for p in game._p1:
                    if p.is_king():
                        bot_score += 5000
                    else:
                        bot_score += 3000
                        row, _ = p.get_pos()
                        bot_potential += row
                for p in game._p2:
                    if p.is_king():
                        opp_score += 5000
                    else:
                        opp_score += 3000
                        row, _ = p.get_pos()
                        opp_potential += (game._board.height() - row)
                bot_potential = (bot_potential / len(game._p1)) * 10
                opp_potential = (opp_potential / len(game._p2)) * 10
                bot_score += bot_potential
                opp_score += opp_potential
            else:
                for p in game._p1:
                    if p.is_king():
                        opp_score += 5000
                    else:
                        opp_score += 3000
                        row, _ = p.get_pos()
                        opp_potential += row
                for p in game._p2:
                    if p.is_king():
                        bot_score += 5000
                    else:
                        bot_score += 3000
                        row, _ = p.get_pos()
                        bot_potential += (game._board.height() - row)
                bot_potential = (bot_potential / len(game._p1)) * 10
                opp_potential = (opp_potential / len(game._p2)) * 10
                bot_score += bot_potential
                opp_score += opp_potential
            return bot_score - opp_score


#
# SIMULATION CODE
#

class BotPlayer:
    """
    Simple class to store information about a bot player in a simulation
    """

    def __init__(self, name, game, bot_player, opp_player):
        """
        Constructor

        Parameters:
          name: str: Name of the bot
          game: Checkers: the game of checkers to play on
          bot_player: Player: bot's player identity
          opp_player: Player: opponent's player identity
        """
        self.name = name
        if self.name == "random":
            self.bot = RandomBot(game, bot_player, opp_player)
        elif self.name == "smart":
            self.bot = SmartBot(game, bot_player, opp_player)
        self.player = bot_player
        self.wins = 0


def simulate(game, n, bots):
    """
    Simulates multiple games between two bots

    Parameters:
      game: Checkers: the game of checkers to play on
      n: int: the number of matches to play
      bots: dict: dictionary mapping player identities to BotPlayer objects (the
                    bots that will face off in each match)

    Returns: None
    """
    for _ in range(n):
        game.new_game()

        while not game._game_over:
            current = bots[game.get_turn()]
            move = current.bot.suggest_move()
            print(f"{current.name} suggested_move:", move)
            game.move(move[0], move[1])
            print(game)

        if game._winner is not None:
            bots[game._winner].wins += 1


@ click.command(name="checkers-bot")
@ click.option('-n', '--num-games', type=click.INT, default=100)
@ click.option('--player1', type=click.Choice(['random', 'smart'],
                                              case_sensitive=False), default="random")
@ click.option('--player2', type=click.Choice(['random', 'smart'],
                                              case_sensitive=False), default="random")
def cmd(num_games, player1, player2):
    board = Checkers(3)

    bot1 = BotPlayer(player1, board, Player.TOP, Player.BOTTOM)
    bot2 = BotPlayer(player2, board, Player.BOTTOM, Player.TOP)

    bots = {Player.TOP: bot1, Player.BOTTOM: bot2}

    simulate(board, num_games, bots)

    bot1_wins = bots[Player.TOP].wins
    bot2_wins = bots[Player.BOTTOM].wins
    ties = num_games - (bot1_wins + bot2_wins)

    print(f"Bot 1 ({player1}) wins: {100 * bot1_wins / num_games:.2f}%")
    print(f"Bot 2 ({player2}) wins: {100 * bot2_wins / num_games:.2f}%")
    print(f"Ties: {100 * ties / num_games:.2f}%")


if __name__ == "__main__":
    cmd()
