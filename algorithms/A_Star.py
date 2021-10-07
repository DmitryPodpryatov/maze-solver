from .Errors import NoSolutionsError
from .Solver import Solver

import heapq
import math
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

        self.heuristics = ['euclidean', 'cosine', 'manhattan', 'complex']

        if heuristic not in self.heuristics:
            raise self.InvalidHeuristicError(f'Invalid heuristic method. Must be one of {self.heuristics}')

        self.heuristic_type = heuristic

    def solve(self, debug: bool = False) -> np.ndarray:
        """
        Given an image of a maze, solve it and return a solution path
        """
        coords = self.start
        priority_queue = [(0, 0, coords, [coords])]  # Loss must go first!
        heapq.heapify(priority_queue)

        while priority_queue:
            _, distance_, coords, path = heapq.heappop(priority_queue)

            neighbors = self.neighbors(coords)
            # all_losses = [distance_ + self.heuristic(n) for n in neighbors]
            all_losses = [self.heuristic(n) for n in neighbors]

            not_visited = [n for n in neighbors if n in set(neighbors) - set(path)]  # Preserve order
            losses = [all_losses[i] for i in range(len(all_losses))
                      if neighbors[i] in not_visited]

            for loss, neighbor in [(loss, n) for loss, n in sorted(zip(losses, not_visited))]:
                if neighbor == self.finish:
                    coords = neighbor
                    self.path = np.array(path + [neighbor])
                    priority_queue = []
                    break
                else:
                    # heapq.heappush(priority_queue, (distance_ + 1 + loss, distance_ + 1, neighbor, path + [neighbor]))
                    heapq.heappush(priority_queue, (loss, distance_ + 1, neighbor, path + [neighbor]))

            if debug:
                print(coords)
                # print(neighbors)
                # print(losses)
                print([(loss, n) for loss, n in sorted(zip(losses, not_visited))])

        if coords != self.finish:
            if debug:
                print(coords, self.finish)

            raise NoSolutionsError('No solution has been found.')
        else:
            print('Solution has been found!')

        return self.path

    def heuristic(self, coords: tuple[int, int]):
        if self.heuristic_type == 'euclidean':
            return self.__euclidean_distance(coords)
        elif self.heuristic_type == 'cosine':
            return self.__cosine_distance(coords)
        elif self.heuristic_type == 'manhattan':
            return self.__manhattan_distance(coords)
        elif self.heuristic_type == 'complex':
            return self.__complex_distance(coords)

    def __euclidean_distance(self, coords: tuple[int, int]):
        y, x = coords
        y_f, x_f = self.finish

        return math.sqrt((x - x_f) ** 2 + (y - y_f) ** 2)

    def __cosine_distance(self, coords: tuple[int, int]):
        return 1000 * distance.cosine(coords, self.finish)

    def __manhattan_distance(self, coords: tuple[int, int]):
        y, x = coords
        y_f, x_f = self.finish

        return abs(x - x_f) + abs(y - y_f)

    def __complex_distance(self, coords: tuple[int, int]):
        return self.__cosine_distance(coords) + self.__manhattan_distance(coords)
