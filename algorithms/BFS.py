from .Errors import NoSolutionsError
from .Solver import Solver

import numpy as np


class BFS(Solver):
    """
    Breadth-first search
    """

    def solve(self, debug: bool = False) -> np.ndarray:
        """
        Given an image of a maze, solve it and return a solution path
        """
        coords = self.start
        stack = [(coords, [coords])]

        while stack:
            coords, path = stack.pop(0)

            neighbors = self.neighbors(coords)

            for neighbor in set(neighbors) - set(path):
                if neighbor == self.finish:
                    coords = neighbor
                    self.path = np.array(path + [neighbor])
                    stack = []
                    break
                else:
                    stack.append((neighbor, path + [neighbor]))

            if debug:
                print(stack)

        if coords != self.finish and len(stack) == 0:
            if debug:
                print(coords, self.finish)

            raise NoSolutionsError('No solution has been found.')
        else:
            print('Solution has been found!')

        return self.path
