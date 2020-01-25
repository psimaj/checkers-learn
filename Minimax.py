import random

from copy import deepcopy

INF = 1000

class Node:

    def __init__(self, state, move):
        self.state = deepcopy(state)
        if move is not None:
            self.state.perform_action(move)
        self.moves = state.get_viable_moves()
        self.children = {}

    def expand(self):
        for move in self.moves:
            self.children[move] = Node(self.state, move)

class Minimax:

    def __init__(self, state, depth):
        self.state = state
        self.max_depth = depth

    def get_best_move(self):
        _, move = self.evaluate_tree(1, Node(self.state, None), -INF, INF)
        return move

    def evaluate_tree(self, depth, node, alpha, beta):
        if depth <= self.max_depth:
            node.expand()
        if node.state.player == 0: #maximizing
            best_value, best_move = -INF, None
            for move, child in node.children.items():
                if best_move is None:
                    best_move = move
                if depth < self.max_depth:
                    value, _ = self.evaluate_tree(depth+1, child, alpha, beta)
                else:
                    value = self.heuristic_evaluation(child.state)
                if value > best_value:
                    best_value, best_move = value, move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value, best_move
        else: #minimizing
            best_value, best_move = INF, None
            for move, child in node.children.items():
                if depth < self.max_depth:
                    value, _ = self.evaluate_tree(depth+1, child, alpha, beta)
                else:
                    value = self.heuristic_evaluation(child.state)
                if value < best_value:
                    best_value, best_move = value, move
                alpha = min(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value, best_move

    def heuristic_evaluation(self, state):
        maxi, mini = 0, 0
        for i in range(state.board_size):
            for j in range(state.board_size):
                f = state.get_field((i, j))
                if f >= 0:
                    if f % 2 == 0:
                        maxi += f + 3
                    else:
                        mini += f + 2
        maxi += random.randint(0, 1)
        mini += random.randint(0, 1)
        return maxi - mini
