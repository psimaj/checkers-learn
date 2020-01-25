import random

from Checkers import GamePlayer

class RandomPlayer(GamePlayer):

    def take_turn(self, state):
        moves = state.get_viable_moves()
        if len(moves) == 0:
            return
        ind = random.randint(0, len(moves) - 1)
        state.perform_action(moves[ind])
        return moves[ind]

    def move_made(self, move):
        pass


class ManualPlayer(GamePlayer):

    def take_turn(self, state):
        moves = state.get_viable_moves()
        if len(moves) == 0:
            return
        move = self.read_move()
        while move not in moves:
            print("Illegal move, try again")
            move = self.read_move()
        state.perform_action(move)
        return move

    def read_move(self):
        try:
            a, b, c, d = [int(x) for x in input().split()]
        except ValueError:
            return None
        return ((a-1, b-1), (c-1, d-1))

    def move_made(self, move):
        pass


import MonteCarloTreeSearch

class MonteCarloPlayer(GamePlayer):

    def __init__(self, max_iterations):
        self.max_iterations = max_iterations
        self.tree = MonteCarloTreeSearch.Tree()

    def set_game(self, game):
        super(MonteCarloPlayer, self).set_game(game)
        self.tree.set_game(game)

    def take_turn(self, state):
        for i in range(self.max_iterations):
            self.tree.perform_iteration()
        move = self.tree.get_best_move()
        state.perform_action(move)
        return move

    def move_made(self, move):
        self.tree.advance_root(move)


import Minimax

class MinimaxPlayer(GamePlayer):

    def __init__(self, depth):
        self.depth = depth

    def set_game(self, game):
        super(MinimaxPlayer, self).set_game(game)
        self.state = game.state

    def take_turn(self, state):
        decider = Minimax.Minimax(state, self.depth)
        move = decider.get_best_move()
        state.perform_action(move)
        return move

    def move_made(self, move):
        pass


class EnMassePlayer(GamePlayer):

    def take_turn(self, state):
        moves = state.get_viable_moves()
        if len(moves) == 0:
            return
        best_move = moves[0]
        if state.player == 0:
            for move in moves[1:]:
                if move[0][0] <= best_move[0][0]:
                    if move[0][1] < best_move[0][1]:
                        best_move = move
                    if move[0][0] < best_move[0][0]:
                        best_move = move
        else:
            for move in moves[1:]:
                if move[0][0] >= best_move[0][0]:
                    if move[0][1] > best_move[0][1]:
                        best_move = move
                    if move[0][0] > best_move[0][0]:
                        best_move = move
        state.perform_action(best_move)
        return best_move

    def move_made(self, move):
        pass


class FlankingPlayer(GamePlayer):

    def take_turn(self, state):
        moves = state.get_viable_moves()
        if len(moves) == 0:
            return
        best_move = moves[0]
        if state.player == 0:
            for move in moves[1:]:
                if move[0][1] <= best_move[0][1]:
                    if move[0][0] < best_move[0][0]:
                        best_move = move
                    if move[0][1] < best_move[0][1]:
                        best_move = move
        else:
            for move in moves[1:]:
                if move[0][1] >= best_move[0][1]:
                    if move[0][0] > best_move[0][0]:
                        best_move = move
                    if move[0][1] > best_move[0][1]:
                        best_move = move
        state.perform_action(best_move)
        return best_move

    def move_made(self, move):
        pass


class AggressivePlayer(GamePlayer):

    def take_turn(self, state):
        moves = state.get_viable_moves()
        if len(moves) == 0:
            return
        best_move = moves[0]
        if state.player == 0:
            for move in moves[1:]:
                if move[0][0] >= best_move[0][0]:
                    if move[0][1] < best_move[0][1]:
                        best_move = move
                    if move[0][0] > best_move[0][0]:
                        best_move = move
        else:
            for move in moves[1:]:
                if move[0][0] <= best_move[0][0]:
                    if move[0][1] > best_move[0][1]:
                        best_move = move
                    if move[0][0] < best_move[0][0]:
                        best_move = move
        state.perform_action(best_move)
        return best_move

    def move_made(self, move):
        pass
