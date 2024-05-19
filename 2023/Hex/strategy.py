from abc import ABC, abstractmethod
from orientation import Orientation
import numpy as np
from random import choice


def distance(grid, orientation):
    opposite = Orientation.COL if orientation == Orientation.ROW else Orientation.ROW
    nb_rows, nb_cols = grid.shape
    to_be_visited = {(i, j) for i in range(nb_rows) for j in range(nb_cols) if grid[i, j] != opposite}
    dist = {cell: np.inf for cell in to_be_visited}
    for cell in to_be_visited:
        if cell[0] == 0 and orientation == Orientation.ROW:
            dist[cell] = 0 if grid[cell] == Orientation.ROW else 1
        if cell[1] == 0 and orientation == Orientation.COL:
            dist[cell] = 0 if grid[cell] == Orientation.COL else 1
    while len(to_be_visited) > 0:
        min_dist = np.inf
        min_dist_cell = None
        for cell in to_be_visited:
            if dist[cell] < min_dist:
                min_dist = dist[cell]
                min_dist_cell = cell
        if min_dist_cell is not None:
            for neighbour in grid.neighbours(min_dist_cell):
                if neighbour in to_be_visited:
                    dist[neighbour] = min(dist[neighbour], min_dist + (0 if grid[neighbour] == orientation else 1))
            to_be_visited.remove(min_dist_cell)
        else:
            break
    if orientation == Orientation.ROW:
        last = [dist[cell] for cell in dist if cell[0] == nb_rows - 1]
    else:
        last = [dist[cell] for cell in dist if cell[1] == nb_cols - 1]
    return min(last) if last else np.inf


def evaluation_minimum_path(grid, orientation):
    opposite = Orientation.COL if orientation == Orientation.ROW else Orientation.ROW
    d1 = distance(grid, orientation)
    d2 = distance(grid, opposite)
    if d1 == 0:
        return np.inf
    if d2 == 0:
        return -np.inf
    return np.log(d2 / d1)


class Strategy(ABC):

    @abstractmethod
    def best_move(self, grid, orientation=None):
        pass


class MiniMaxStrategy(Strategy):
    def __init__(self, evaluation, depth):
        self.evaluation = evaluation
        self.depth = depth

    def minimax(self, grid, depth, orientation=None):
        opposite = Orientation.COL if orientation == Orientation.ROW else Orientation.ROW
        if grid.is_winner(orientation):
            return (None, np.inf) if orientation == Orientation.ROW else (None, -np.inf)
        if grid.is_winner(opposite):
            return (None, -np.inf) if orientation == Orientation.ROW else (None, np.inf)
        if depth == 0:
            return None, self.evaluation(grid, orientation)
        nb_rows, nb_cols = grid.shape
        best = (None, -np.inf) if orientation == Orientation.ROW else (None, np.inf)
        for i in range(nb_rows):
            for j in range(nb_cols):
                g = grid.copy()
                if g[i, j] == 0:
                    g[i, j] = orientation
                    _, value = self.minimax(g, depth - 1, opposite)
                    if orientation == Orientation.ROW and value >= best[1]:
                        best = (i, j), value
                    if orientation == Orientation.COL and value <= best[1]:
                        best = (i, j), value
        return best

    def best_move(self, grid, orientation=None):
        return self.minimax(grid, self.depth, orientation)[0]


class RandomStrategy(Strategy):
    def best_move(self, grid, orientation=None):
        nb_rows, nb_cols = grid.shape
        empty_cells = [(i, j) for i in range(nb_rows) for j in range(nb_cols) if grid[i, j] == 0]
        return choice(empty_cells) if len(empty_cells) > 0 else None
