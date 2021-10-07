from .Errors import NoSolutionsError
from .Solver import Solver

import numpy as np


class Maze(Solver):

    def solve(self, debug: bool = False) -> np.ndarray:
        pass
