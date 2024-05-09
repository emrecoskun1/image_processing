import cv2
import numpy as np
import matplotlib.pyplot as plt


def convolution(image, kernel):
    """
    Resim ve çekirdek arasında konvolüsyon işlemi yapar.

    Args:
    image (numpy.ndarray): Giriş resmi.
    kernel (numpy.ndarray): Konvolüsyon çekirdeği.

    Returns:
    numpy.ndarray: Konvolüsyon sonucu.
    """
    image_height, image_width = image.shape[:2]
    kernel_height, kernel_width = kernel.shape

    # Çıktı resminin boyutlarını hesapla
    output_height = image_height - kernel_height + 1
    output_width = image_width - kernel_width + 1

    # Çıktı matrisini oluştur
    output = np.zeros((output_height, output_width))

    # Konvolüsyon işlemi
    for i in range(output_height):
        for j in range(output_width):
            # Giriş resimindeki bir bölgeyi al
            image_patch = image[i : i + kernel_height, j : j + kernel_width]
            # Konvolüsyon işlemi
            output[i, j] = np.mean(image_patch * kernel)

    return output
