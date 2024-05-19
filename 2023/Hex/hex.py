import numpy as np
from orientation import Orientation
from grid import HexGrid
from player import Player
from strategy import MiniMaxStrategy, evaluation_minimum_path, RandomStrategy


class HexGame:
    def __init__(self, size):
        self.player1 = Player(Orientation.ROW, MiniMaxStrategy(evaluation_minimum_path, 3))
        self.player2 = Player(Orientation.COL, MiniMaxStrategy(evaluation_minimum_path, 3))
        # self.player2 = Player(Orientation.COL, RandomStrategy())
        self.grid = HexGrid(np.zeros((size, size)))

    def play(self):
        current_player = self.player2
        while True:
            pos = current_player.play(self.grid)
            if pos is None:
                break
            self.grid[pos] = current_player.orientation
            print('PLAYER ' + str(current_player.orientation))
            print(self.grid)
            print('-----')
            if self.grid.is_winner(current_player.orientation):
                print('PLAYER ' + str(current_player.orientation) + ' WINS')
                break
            current_player = self.player2 if current_player == self.player1 else self.player1


game = HexGame(4)
game.play()
