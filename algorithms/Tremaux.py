from .Errors import NoSolutionsError
from .Solver import Solver

import numpy as np
from collections import Counter


class Tremaux(Solver):
    """
    Tremaux's algorithm
    """

    def solve(self, debug: bool = False) -> np.ndarray:
        """
        Given an image of a maze, solve it and return a solution path
        """
        coords = self.start
        #stack = [(coords, [coords])]

        path = [coords]
        DEADEND = False
        i = 0
        CHECK = 0
        
        while path[-1] != self.finish:
            coords = path[i]
            neighbors = self.neighbors(coords)
            #if CHECK != 0:
            #    print('Info after deadend')
            #    print('Point:', coords)
            #    print('Nei', neighbors)
            if len(neighbors) == 1 and neighbors[0] in path:
                DEADEND = True
                #print('Find deadend', i)
                #print(path)

            if not DEADEND:
                for x in neighbors:
                    if x not in path:
                        path.append(x)
                        i = len(path)-1
                        break
            else:
                while len(set(neighbors)-set(path)) < 1:
                    path.append(path[i])
                    i-=1
                    neighbors = self.neighbors(path[i])
                DEADEND = False
                CHECK = i
                #print('Close deadend', i)
                #print(path)

            if debug:
                if len(path)%20 == 0:
                    print(path)

        if coords != self.finish and len(path) == 0:
            if debug:
                print(coords, self.finish)

            raise NoSolutionsError('No solution has been found.')
        else:
            print('Solution has been found!')

        count = Counter(path)
        self.path = [point for point in count if count[point]==1]
        return self.path