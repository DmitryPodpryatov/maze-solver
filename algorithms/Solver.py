from abc import ABC, abstractmethod
from random import shuffle

import cv2
import numpy as np

from algorithms.Errors import InvalidStartError, InvalidFinishError, InvalidImageError


class Solver(ABC):
    """
    Abstract class for maze-solving algorithms

    255 in the image is path and 0 is a wall
    """

    def __init__(self, image: np.ndarray, start: tuple[int, int], finish: tuple[int, int]) -> None:
        """
        :param image: input image
        :param start: coordinates of the beginning of the maze
        :param finish: coordinates of the end of the maze
        """
        self.image = image.copy()
        self.height, self.width = self.image.shape
        self.start = start
        self.finish = finish
        self.path = np.array([])

        if len(self.image.shape) > 2:
            raise InvalidImageError('Image must be gray!')

        if self.image[self.start] != 255:
            raise InvalidStartError(f'Start value should be 255, it is {self.image[self.start]}')

        if self.image[self.finish] != 255:
            raise InvalidFinishError(f'Finish value should be 255, it is {self.image[self.finish]}')

    @abstractmethod
    def solve(self) -> np.ndarray:
        """
        Given an image of a maze, solve it and return a solution path
        """
        pass

    def draw(self, image: np.ndarray = None, thickness: int = 1) -> np.ndarray:
        """
        Draws the path on the input image

        :return: new image with the drawn path
        """
        image = image.copy()

        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)

        # Convert to cartesian coordinates for utils
        # See https://stackoverflow.com/a/18817152/11109151 for explanation of `np.int32`
        path = np.int32([self.__matrix_to_cartesian(self.path)])

        # Draw the path
        image = cv2.polylines(image, path, isClosed=False, color=red, thickness=thickness)

        # Draw start and finish dots
        if thickness == 1:
            image[self.start] = green
            image[self.finish] = blue
        else:
            image = cv2.circle(image, self.__coords_to_cartesian(self.start), radius=thickness, color=green,
                               thickness=-1)
            image = cv2.circle(image, self.__coords_to_cartesian(self.finish), radius=thickness, color=blue,
                               thickness=-1)

        return image

    def neighbors(self, coords: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Return all neighbors' coordinates of the pixel at `coords`
        """
        y, x = coords

        left = (y - 1, x) if y > 0 else None
        right = (y + 1, x) if y < self.width - 1 else None
        top = (y, x - 1) if x > 0 else None
        bottom = (y, x + 1) if x < self.height - 1 else None

        ns = [left, right, top, bottom]
        shuffle(ns)  # Randomly rearrange list to prevent algorithm from going some way first

        return [n for n in ns
                if n is not None and self.image[n] == 255]

    def __matrix_to_cartesian(self, path: np.ndarray) -> np.ndarray:
        new_path = path.copy()

        for i, coords in enumerate(path):
            new_path[i] = self.__coords_to_cartesian(coords)

        return new_path

    @staticmethod
    def __coords_to_cartesian(coords: tuple[int, int]) -> tuple[int, int]:
        """
        Convert coordinates in the matrix notation to the cartesian coordinates

        >>> solver = ... # Initialize Solver with image 4x5 (width x height)
        >>> solver.__matrix_to_cartesian((2, 2))
        [(2, 1)]
        """
        y, x = coords
        return x, y
