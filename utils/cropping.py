import cv2
import numpy as np


def crop(image: np.ndarray, points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    :param image: input image as numpy array
    :param points: points of the cropping part in order
        top left, bottom left, top right, bottom right.
        Note: must be a float32 numbers
    :return: cropped image as numpy array and a matrix for inverse transform
    """
    (x1, y1), _, _, (x4, y4) = points
    transformed_points = np.float32([[0, 0], [x4 - x1, 0], [0, y4 - y1], [x4 - x1, y4 - y1]])

    cropped = image.copy()

    M = cv2.getPerspectiveTransform(points, transformed_points)
    M_inv = np.linalg.inv(M)

    cropped = cv2.warpPerspective(cropped, M, cropped.shape[:2])

    return cropped[:int(y4 - y1), :int(x4 - x1)], M_inv


def draw_solution_on_source_image(source: np.ndarray, cropped: np.ndarray, M_inv: np.ndarray) -> np.ndarray:
    inversed = inverse_crop(cropped, M_inv, source.shape[:2][::-1])

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    coords_red = []
    coords_green = []
    coords_blue = []

    for i, row in enumerate(inversed):
        for j, rgb in enumerate(row):
            if np.array_equal(rgb, red):
                coords_red.append((i, j))
            elif np.array_equal(rgb, green):
                coords_green.append((i, j))
            elif np.array_equal(rgb, blue):
                coords_blue.append((i, j))

    result = source.copy()

    for coords in coords_red:
        result[coords] = red

    for coords in coords_green:
        result[coords] = green

    for coords in coords_blue:
        result[coords] = blue

    return result


def inverse_crop(image: np.ndarray, M: np.ndarray, out_shape: tuple[int, int]) -> np.ndarray:
    uncropped = image.copy()
    uncropped = cv2.warpPerspective(uncropped, M, out_shape)

    return uncropped
