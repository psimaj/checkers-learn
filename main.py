#!/usr/bin/python3.6

import Checkers
import Players

mcp_iterations = 100
minimax_depth = 4
wins = [0, 0]
iterations = 50
for i in range(iterations):
    game = Checkers.Game()
    #visualizer = Checkers.TerminalGameVisualizer(game)
    player_one = Players.MinimaxPlayer(minimax_depth)
    player_two = Players.MonteCarloPlayer(mcp_iterations)
    runner = Checkers.GameRunner(game, player_one, player_two)
    result = runner.run()
    if result is not None:
        wins[result] += 1
    print(i, result)
draws = iterations - wins[0] - wins[1]
print("1: %d, 2: %d, D: %d" % (wins[0], wins[1], draws))
