from .Errors import NoSolutionsError
from .Solver import Solver

import numpy as np


class Maze(Solver):
    """
    Depth-first search
    """

    def solve(self, debug: bool = False) -> np.ndarray:
        """
        Given an image of a maze, solve it and return a solution path
        """
        self.path = []

        return self.path
