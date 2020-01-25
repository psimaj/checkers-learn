import abc

from util import add, div

class GameState:

    def __init__(self):
        self.board_size = 8
        self.pawn_rows = 3
        self.game_ended = False
        self.board = [[-1 for i in range(self.board_size)] for j in range(self.board_size)]
        self.movement_vectors = (((1, -1), (1, 1)), ((-1, -1), (-1, 1)))
        self.pacifist_turns = 0
        self.reset()

    def get_winner(self):
        if not self.game_ended:
            return None
        if self.game_drawn:
            return None
        return 1 - self.player

    def reset(self):
        self.player = 0
        self.only_viable_field = None
        self.game_ended = False
        self.game_drawn = False
        for i in range(0, self.pawn_rows):
            for j in range(0, self.board_size, 2):
                self.board[i][j + ((i + 1) % 2)] = -1
                self.board[i][j + (i % 2)] = 0
        for i in range(self.pawn_rows, self.board_size - self.pawn_rows):
            self.board[i] = [-1] * self.board_size
        for i in range(self.board_size - self.pawn_rows, self.board_size):
            for j in range(0, self.board_size, 2):
                self.board[i][j + ((i + 1) % 2)] = -1
                self.board[i][j + (i % 2)] = 1

    def get_field(self, field):
        i, j = field
        if i >= self.board_size or i < 0 or j >= self.board_size or j < 0:
            return None
        return self.board[i][j]


    def get_viable_moves(self):
        if not self.only_viable_field is None:
            return self.get_viable_moves_from_field(self.only_viable_field)[1]
        jumps = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                field = self.get_field((i, j))
                if field != None and field >= 0 and field % 2 == self.player:
                    self.gather_viable_jumps((i, j), jumps)
        if len(jumps) > 0:
            return jumps
        walks = []
        kings = [0,0]
        pawns = 0
        kings_pos = [None, None]
        for i in range(self.board_size):
            for j in range(self.board_size):
                field = self.get_field((i, j))
                if field > 1:
                    kings[field % 2] += 1
                    kings_pos[field % 2] = (i, j)
                elif field >= 0:
                    pawns += 1
                if field >= 0 and field % 2 == self.player:
                    self.gather_viable_walks(self.player, (i, j), walks)
                    if field > 1:
                        self.gather_viable_walks(1 - self.player, (i, j), walks)
        if self.pacifist_turns >= 50:
            self.game_drawn = True
        if pawns == 0 and kings[0] == kings[1] and kings[0] == 1:
            diff_y = abs(kings_pos[0][0] - kings_pos[1][0])
            diff_x = abs(kings_pos[0][1] - kings_pos[1][1])
            if diff_y > 1 or diff_x > 1:
                self.game_drawn = True
        if len(walks) == 0 or self.game_drawn:
            self.game_ended = True
        return walks


    def get_walk(self, origin, vector):
        destination = add(origin, vector)
        destination_state = self.get_field(destination)
        if destination_state == -1:
            return (origin, destination)
        return None


    def get_jump(self, origin, vector):
        destination = add(origin, vector)
        destination_state = self.get_field(destination)
        if destination_state == None or destination_state == -1:
            return None
        if destination_state % 2 != self.player:
            destination = add(destination, vector)
            destination_state = self.get_field(destination)
            if destination_state == -1:
                return (origin, destination)
        return None


    def gather_viable_walks(self, direction, field, walks):
        for vector in self.movement_vectors[direction]:
            move = self.get_walk(field, vector)
            if move is not None:
                walks.append(move)


    def gather_viable_jumps(self, field, jumps):
        for vector in self.movement_vectors[0] + self.movement_vectors[1]:
            move = self.get_jump(field, vector)
            if move is not None:
                jumps.append(move)


    def get_viable_moves_from_field(self, field):
        jumps = []
        self.gather_viable_jumps(field, jumps)
        if len(jumps) > 0:
            return 1, jumps
        figure = self.get_field(field)
        walks = []
        self.gather_viable_walks(self.player, field, walks)
        if figure > 1:
            self.gather_viable_walks(1 - self.player, field, walks)
        return 0, walks


    def perform_action(self, move):
        if move is None:
            self.game_ended = True
            return
        origin, destination = move
        figure = self.get_field(origin)
        if figure == 0 and destination[0] == self.board_size - 1:
            figure = 2
        if figure == 1 and destination[0] == 0:
            figure = 3
        self.add_figure(figure, destination)
        self.remove_figure(origin)
        if abs(move[0][0] - move[1][0]) == 2:
            self.pacifist_turns = 0
            half_destination = div(add(origin, destination), 2)
            self.remove_figure(half_destination)
            move_type, _ = self.get_viable_moves_from_field(destination)
            if move_type == 1:
                self.only_viable_field = destination
            else:
                self.only_viable_field = None
                self.player = 1 - self.player
        else:
            self.pacifist_turns += 1
            self.player = 1 - self.player


    def add_figure(self, figure, field):
        self.set_field(field, figure)


    def remove_figure(self, field):
        self.set_field(field, -1)


    def set_field(self, field, value):
        self.board[field[0]][field[1]] = value

class Game:

    def __init__(self):
        self.state = GameState()
        self.observers = []
        self.players = [None, None]

    def play(self):
        self.state.reset()
        self.notify_board_changed()
        self.notify_turn_passed()
        while True:
            move = self.players[self.state.player].take_turn(self.state)
            self.notify_move_made(move)
            self.notify_board_changed()
            if self.state.game_ended:
                self.notify_game_ended()
                return self.state.get_winner()
            self.notify_turn_passed()

    def notify_move_made(self, move):
        for i in range(2):
            self.players[i].move_made(move)

    def notify_board_changed(self):
        for obs in self.observers:
            obs.board_changed()

    def notify_turn_passed(self):
        for obs in self.observers:
            obs.turn_passed(self.state.player)

    def notify_game_ended(self):
        for obs in self.observers:
            obs.game_ended(self.state.get_winner())

    def add_observer(self, observer):
        self.observers.append(observer)


    def add_player(self, player, player_index):
        self.players[player_index-1] = player


class GameObserver(metaclass = abc.ABCMeta):

    def __init__(self, game):
        self.game = game
        game.add_observer(self)

    @abc.abstractmethod
    def board_changed(self):
        pass

    @abc.abstractmethod
    def game_ended(self, winner):
        pass

    @abc.abstractmethod
    def turn_passed(self, passed_to):
        pass

class GamePlayer(metaclass = abc.ABCMeta):

    def set_game(self, game):
        self.game = game


    def set_index(self, player_index):
        self.player_index = player_index - 1
        self.game.add_player(self, player_index)

    @abc.abstractmethod
    def take_turn(self, moves):
        pass

    @abc.abstractmethod
    def move_made(self, move):
        pass

class GameRunner:

    def __init__(self, game, player_one, player_two):
        self.game = game
        player_one.set_game(game)
        player_two.set_game(game)
        player_one.set_index(1)
        player_two.set_index(2)


    def run(self):
        return self.game.play()

class TerminalGameVisualizer(GameObserver):

    def __init__(self, game):
        super(TerminalGameVisualizer, self).__init__(game)
        self.visual_encoding = {
            -1: '_',
            0: '1',
            1: '2',
            2: 'A',
            3: 'B',
        }


    def board_changed(self):
        self.print_board()


    def game_ended(self, player):
        if player is None:
            message = "Draw"
        else:
            message = "Player %d has won" % (player + 1)
        print(message)


    def turn_passed(self, passed_to):
        print("Player %d taking turn" % (passed_to + 1))


    def print_board(self):
        for i in range(self.game.state.board_size-1, -1, -1):
            self.print_row(i)
        print('X ', end='')
        print(*[str(i+1) for i in range(self.game.state.board_size)])


    def print_row(self, i):
        print(str(i+1) + '|', end='')
        for j in range(self.game.state.board_size):
            print(self.visual_encoding[self.game.state.get_field((i, j))] + '|', end='')
        print()
