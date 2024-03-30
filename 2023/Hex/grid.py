import numpy as np
from collections import deque
from orientation import Orientation


class HexGrid(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

    def neighbours(self, cell):
        nb_rows, nb_cols = self.shape
        potential_neighbours = [(cell[0] + 1, cell[1]),
                                (cell[0] - 1, cell[1]),
                                (cell[0], cell[1] + 1),
                                (cell[0], cell[1] - 1),
                                (cell[0] - 1, cell[1] + 1),
                                (cell[0] + 1, cell[1] - 1),
                                ]
        return [neighbour for neighbour in potential_neighbours if
                0 <= neighbour[0] < nb_rows and 0 <= neighbour[1] < nb_cols]

    def is_winner(self, orientation):
        nb_rows, nb_cols = self.shape
        stack = deque(
            [(0, k) for k in range(nb_cols) if self[0, k] == orientation]) if orientation == Orientation.ROW else deque(
            [(k, 0) for k in range(nb_rows) if self[k, 0] == orientation])
        visited = []
        while len(stack) > 0:
            cell = stack.pop()
            if (cell[0] == nb_rows - 1 and orientation == Orientation.ROW) or (
                    cell[1] == nb_cols - 1 and orientation == Orientation.COL):
                return True
            visited.append(cell)
            for neighbour in self.neighbours(cell):
                if self[neighbour] == orientation and neighbour not in visited:
                    stack.append(neighbour)
        return False
