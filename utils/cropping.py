import cv2
import numpy as np


def crop(image: np.ndarray, points: np.ndarray) -> np.ndarray:
    """
    :param image: input image as numpy array
    :param points: points of the cropping part in order
        top left, bottom left, top right, bottom right.
        Note: must be a float32 numbers
    :return: cropped image as numpy array
    """
    (x1, y1), _, _, (x4, y4) = points
    transformed_points = np.float32([[0, 0], [x4 - x1, 0], [0, y4 - y1], [x4 - x1, y4 - y1]])

    cropped = image.copy()

    M = cv2.getPerspectiveTransform(points, transformed_points)
    cropped = cv2.warpPerspective(cropped, M, cropped.shape[:2])

    return cropped[:int(y4 - y1), :int(x4 - x1)]
