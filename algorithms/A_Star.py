from .Errors import NoSolutionsError
from .Solver import Solver

import numpy as np


class A_Star(Solver):
    """
    A*
    """

    def solve(self, debug: bool = False) -> np.ndarray:
        """
        Given an image of a maze, solve it and return a solution path
        """
        coords = self.start

        pass

        if coords != self.finish:
            if debug:
                print(coords, self.finish)

            raise NoSolutionsError('No solution has been found.')
        else:
            print('Solution has been found!')

        return self.path
