import random

import numpy as np

from copy import deepcopy

class Node:

    def __init__(self, parent):
        self.parent = parent
        self.children = {}
        self.moves = None
        self.visited_children = 0
        self.visited = False
        self.wins = 0
        self.visits = 0

    def try_set_moves(self, state):
        self.player = state.player
        if self.moves is None:
            self.moves = state.get_viable_moves()

    def rollout_policy(self):
        if len(self.moves) == 0:
            return None
        return self.moves[random.randint(0, len(self.moves)-1)]

    def expand(self, state):
        self.try_set_moves(state)
        if len(self.moves) > len(self.children):
            for move in self.moves:
                if move not in self.children:
                    self.children[move] = Node(self)

    def is_fully_expanded(self):
        return self.moves is not None and len(self.children) == self.visited_children

    def UCT(self):
        exploitation = self.wins / self.visits
        exploration = np.sqrt(2 * np.log(self.parent.visits) / self.visits)
        return exploitation + exploration

    def get_best_move(self):
        result, max_visits = None, 0
        for move, child in self.children.items():
            if child.visits >= max_visits:
                max_visits = child.visits
                result = move
        return result

    def visit(self, state):
        self.expand(state)
        if not self.visited:
            self.visited = True
            if self.parent is not None:
                self.parent.visited_children += 1

class Tree:

    def __init__(self):
        self.root = Node(None)
        self.original_root = self.root

    def set_game(self, game):
        self.root = self.original_root
        self.state = game.state

    def advance_root(self, move):
        if move not in self.root.children:
            self.root.children[move] = Node(self.root)
        self.root = self.root.children[move]

    def perform_iteration(self):
        tmp_state = deepcopy(self.state)
        leaf = self.search(tmp_state)
        leaf.visit(tmp_state)
        node, winner = self.playout(leaf, tmp_state)
        self.backpropagate(node, winner)

    def get_best_move(self):
        return self.root.get_best_move()

    def search(self, state):
        curr = self.root
        while True:
            curr.expand(state)
            if not curr.visited:
                return curr
            if len(curr.children) == 0:
                return curr
            if curr.is_fully_expanded():
                best_child, best_move, best_UCT = None, None, 0
                for move, child in curr.children.items():
                    if child.UCT() > best_UCT:
                        best_UCT = child.UCT()
                        best_child = child
                        best_move = move
                state.perform_action(best_move)
                curr = best_child
            else:
                for move, child in curr.children.items():
                    if not child.visited:
                        state.perform_action(move)
                        return child

    def playout(self, node, state):
        while True:
            node.expand(state)
            move = node.rollout_policy()
            if move is None:
                #winner = 1 if state.get_winner() == self.state.player else 0
                winner = state.get_winner()
                return node, winner
            else:
                state.perform_action(move)
                node = node.children[move]

    def backpropagate(self, node, winner):
        while True:
            node.visits += 1
            node.wins += 1 if node.player != winner else 0
            #node.wins += winner
            if node.parent is None or node == self.root:
                return
            node = node.parent
