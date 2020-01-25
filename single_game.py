#!/usr/bin/python3.6

import Checkers
import Players
import sys

def get_player(player_type):
    players = {
        'random': Players.RandomPlayer(),
        'manual': Players.ManualPlayer(),
        'monte_carlo': Players.MonteCarloPlayer(100),
        'minimax': Players.MinimaxPlayer(4),
        'en_masse': Players.EnMassePlayer(),
        'flanking': Players.FlankingPlayer(),
        'aggressive': Players.AggressivePlayer(),
    }
    return players[player_type]

player_one = get_player(sys.argv[1])
player_two = get_player(sys.argv[2])

game = Checkers.Game()
visualizer = Checkers.TerminalGameVisualizer(game)
runner = Checkers.GameRunner(game, player_one, player_two)
runner.run()
