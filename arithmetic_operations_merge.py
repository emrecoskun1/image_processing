import cv2
import numpy as np


def merge_images(image1_path, image2_path):
    # İlk resmi oku
    image1 = cv2.imread(image1_path)
    # İkinci resmi oku
    image2 = cv2.imread(image2_path)

    # İki resmin boyutlarını al
    height1, width1, _ = image1.shape
    height2, width2, _ = image2.shape

    # İki resmin en büyük boyutunu bul
    max_width = max(width1, width2)
    max_height = max(height1, height2)

    # İlk resmi yeniden boyutlandır
    resized_image1 = np.zeros((max_height, max_width, 3), dtype=np.uint8)
    resized_image1[:height1, :width1, :] = image1

    # İkinci resmi yeniden boyutlandır
    resized_image2 = np.zeros((max_height, max_width, 3), dtype=np.uint8)
    resized_image2[:height2, :width2, :] = image2

    # İki resmi birbirinden çıkar
    merged_image = np.zeros((max_height, max_width, 3), dtype=np.uint8)
    for i in range(max_height):
        for j in range(max_width):
            pixel1 = resized_image1[i, j]
            pixel2 = resized_image2[i, j]
            merged_pixel = [max(0, pixel1[c] - pixel2[c]) for c in range(3)]
            merged_image[i, j] = merged_pixel

    return merged_image
