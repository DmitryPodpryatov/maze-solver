import math

from .Errors import NoSolutionsError
from .Solver import Solver

import numpy as np
from scipy.spatial import distance


class A_Star(Solver):
    """
    A*
    """

    class InvalidHeuristicError(Exception):
        pass

    def __init__(self, image: np.ndarray,
                 start: tuple[int, int],
                 finish: tuple[int, int],
                 heuristic: str = 'euclidean'):
        super(A_Star, self).__init__(image, start, finish)

        self.heuristics = ['euclidean', 'cosine', 'manhattan']

        if heuristic not in self.heuristics:
            raise self.InvalidHeuristicError(f'Invalid heuristic method. Must be one of {self.heuristics}')

        self.heuristic_type = heuristic

    def solve(self, debug: bool = False) -> np.ndarray:
        """
        Given an image of a maze, solve it and return a solution path
        """
        coords = self.start
        stack = [(coords, [coords], 0)]

        while stack:
            coords, path, dist = stack.pop(0)

            neighbors = self.neighbors(coords)
            losses = [self.heuristic(n) + dist for n in neighbors]
            not_visited = [n for n in neighbors if n in set(neighbors) - set(path)]  # Preserve order
            not_visited_indexes = [neighbors.index(n) for n in not_visited]
            not_visited_losses = [losses[i] for i in not_visited_indexes]

            for neighbor, loss in [(n, loss) for loss, n in sorted(zip(not_visited_losses, not_visited))]:
                if neighbor == self.finish:
                    coords = neighbor
                    self.path = np.array(path + [neighbor])
                    stack = []
                    break
                else:
                    stack.append((neighbor, path + [neighbor], dist + 1))

            if debug:
                print(stack)

        if coords != self.finish and len(stack) == 0:
            if debug:
                print(coords, self.finish)

            raise NoSolutionsError('No solution has been found.')
        else:
            print('Solution has been found!')

        return self.path

    def heuristic(self, coords: tuple[int, int]):
        if self.heuristic_type == "euclidean":
            return self.__euclidean_distance(coords)
        elif self.heuristic_type == "cosine":
            return self.__cosine_distance(coords)
        elif self.heuristic_type == "manhattan":
            return self.__manhattan_distance(coords)

    def __euclidean_distance(self, coords: tuple[int, int]):
        x, y = coords
        x_f, y_f = self.finish

        return math.sqrt((x - x_f) ** 2 + (y - y_f) ** 2)

    def __cosine_distance(self, coords: tuple[int, int]):
        return distance.cosine(coords, self.finish)

    def __manhattan_distance(self, coords: tuple[int, int]):
        x, y = coords
        x_f, y_f = self.finish

        return abs(x - x_f) + abs(y - y_f)
