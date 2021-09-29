import cv2
import matplotlib.pyplot as plt
import numpy as np


def imshow(image: np.ndarray, cmap='rgb') -> None:
    if cmap == 'rgb':
        cmap = None
    elif cmap == 'bgr':
        image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
        cmap = None
    else:
        cmap = 'gray'

    plt.imshow(image, cmap=cmap)
    plt.show()
