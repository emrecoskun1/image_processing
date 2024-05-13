import numpy as np

def convert_gray(image):
    result_image = np.zeros((image.shape[0], image.shape[1], 1), dtype=np.uint8)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            result_image[i, j] = image[i, j, 0] * 0.299 + image[i, j, 1] * 0.587 + image[i, j, 2] * 0.114
    return result_image
