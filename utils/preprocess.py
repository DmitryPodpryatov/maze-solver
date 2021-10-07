import cv2
import numpy as np


def threshold(image, blur_k=None, thresh_k=None):
    h, w = image.shape[:2]

    if not blur_k:
        blur_k = int(min(h, w)//22)
    if blur_k%2 == 0:
        blur_k -= 1

    if not thresh_k:
        thresh_k = int(min(h, w)//6.6)
    if thresh_k%2 == 0:
        thresh_k -= 1

    blur_img = cv2.GaussianBlur(image, (blur_k,blur_k), 1)
    thresh2 = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                          cv2.THRESH_BINARY, thresh_k, 10)
    return thresh2


def get_kernel(kernel_size):
    return np.ones((kernel_size,kernel_size), np.uint8)


def morphological(image, erosion_k=None, dilation_k=None):
    h, w = image.shape[:2]
    
    if not erosion_k:
        erosion_k = int(min(h, w)//30)
    if erosion_k%2 == 0:
        erosion_k-=1
    
    if not dilation_k:
        dilation_k = int(min(h, w)//20)
    if dilation_k%2 == 0:
        dilation_k-=1

    img_erosion = cv2.erode(image, get_kernel(erosion_k), iterations=1)
    img_dilation = cv2.dilate(img_erosion, get_kernel(dilation_k), iterations=1)

    return img_dilation


def resize_image(image, step):
    h, w = image.shape[:2]
    T = int(255/1.2)
    new_image = np.full(image.shape, 0)
    for i in range(0, w, step):
        for j in range(0, h, step):
            area = image[j:j+step, i:i+step]
            if np.mean(area) > T:
                new_image[j:j+step, i:i+step] += 255

    resized_img = cv2.resize(new_image, (new_image.shape[1]//step, new_image.shape[0]//step), interpolation = cv2.INTER_LINEAR_EXACT)
    resized_img[resized_img > 0] = 255
    return resized_img

    
def project_solution(h_source, w_source, h_resized, w_resized, solution):
    new_solution = []
    for x, y in solution:
        new_x = int(w_source*x/w_resized)
        new_y = int(h_source*y/h_resized)
        new_solution.append([new_x, new_y])
    return new_solution


def draw_solution(source_image, new_solution):
    rad = min(source_image.shape[0], source_image.shape[1]) //100
    if rad < 1:
        rad = 1
    for x, y in new_solution:
        cv2.circle(source_image, (y, x), rad, (255, 0, 0), -1)
    return source_image
