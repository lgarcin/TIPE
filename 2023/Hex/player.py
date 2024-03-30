class Player:
    def __init__(self, orientation, strategy):
        self.orientation = orientation
        self.strategy = strategy

    def play(self, grid):
        return self.strategy.best_move(grid, self.orientation)
