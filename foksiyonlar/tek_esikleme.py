import numpy as np


def threshold(image, threshold_value):
    # Boş bir görüntü oluştur
    thresholded_image = np.zeros_like(image)

    # Görüntü boyutları
    rows, cols = image.shape

    # Eşik değeri uygulama
    for i in range(rows):
        for j in range(cols):
            if image[i, j] >= threshold_value:
                thresholded_image[i, j] = 255
            else:
                thresholded_image[i, j] = 0

    return thresholded_image
