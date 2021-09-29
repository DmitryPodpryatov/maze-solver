from .Errors import NoSolutionsError
from .Solver import Solver
from .Maze import Maze

import numpy as np
import cv2
from copy import copy

class Deadend(Solver):
    """
    Deadend algorithm
    """

    def solve(self, debug: bool = False) -> np.ndarray:
        """
        Given an image of a maze, solve it and return a solution path
        """
        #coords = self.start

        def find_deadends(maze):
            #maze = Maze(image, self.start, self.finish)
            deadends = []
            for i in range(maze.height):
                for j in range(maze.width):
                    point = (i, j)
                    if maze.image[i, j] == 255:
                        if len(maze.neighbors(point)) == 1:
                            deadends.append(point)
            if maze.start in deadends:
                deadends.remove(maze.start)
            if maze.finish in deadends:
                deadends.remove(maze.finish)
            return deadends

        all_points = np.squeeze(np.asarray(self.image))
        new_image = copy(self.image)
        maze = Maze(new_image, self.start, self.finish)
        deadends = find_deadends(maze)

        while deadends:
            bad_path = []
            for d in deadends:
                point = d
                neigbours = maze.neighbors(point)
                while len(neigbours) < 3:
                    bad_path.append(point)
                    for neigbour in neigbours:
                        if neigbour not in bad_path:
                            point = neigbour
                            neigbours = maze.neighbors(point)
            for point in bad_path:
                new_image[point] = 0
            maze = Maze(new_image, self.start, self.finish)
            deadends = find_deadends(maze)
        
        path = []
        for i in range(maze.height):
            for j in range(maze.width):
                if maze.image[i, j] == 255:
                    path.append((i, j))
        self.path = path
        return self.path

    def draw(self, image: np.ndarray = None, thickness: int = 1) -> np.ndarray:
        image = image.copy()

        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)

        # Convert to cartesian coordinates for plotting
        # See https://stackoverflow.com/a/18817152/11109151 for explanation of `np.int32`
        path = self.path

        for point in path:
            image[point[0], point[1]] = red

        # Draw start and finish dots
        if thickness == 1:
            image[self.start] = green
            image[self.finish] = blue
        else:
            image = cv2.circle(image, self.start, radius=thickness, color=green, thickness=-1)
            image = cv2.circle(image, self.finish, radius=thickness, color=blue, thickness=-1)

        return image
            
        '''                

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
        '''
        #return deadends
