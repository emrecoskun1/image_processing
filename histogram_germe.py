import cv2
import numpy as np
import matplotlib.pyplot as plt


def calculate_histogram(image):
    # Histogramı hesaplamak için 0'lardan oluşan bir dizi oluştur
    hist = np.zeros(256)

    # Görüntüdeki her piksel değerini dolaşarak histogramı hesapla
    for pixel_value in range(256):
        hist[pixel_value] = np.sum(image == pixel_value)

    return hist


def cumulative_distribution_function(hist):
    # Kumulatif dağılım fonksiyonunu hesapla
    cdf = np.zeros(256)
    cdf[0] = hist[0]

    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + hist[i]

    return cdf


def histogram_stretching(image):
    # Histogramı hesapla
    hist = calculate_histogram(image)

    # Kumulatif dağılımı hesapla
    cdf = cumulative_distribution_function(hist)

    # Minimum ve maksimum değerleri hesapla
    cdf_min = np.min(cdf)
    cdf_max = np.max(cdf)

    # Yeni görüntüyü oluştur
    stretched_image = np.zeros_like(image)
    for pixel_value in range(256):
        stretched_image[image == pixel_value] = (
            (cdf[pixel_value] - cdf_min) / (cdf_max - cdf_min)
        ) * 255

    return stretched_image.astype(np.uint8)


# # Görüntünün dosya yolunu belirle
# image_path = r"C:\Users\yunusemrecoskun\Desktop\cat.jpg"

# # Renkli görüntüyü yükle
# original_image = cv2.imread(image_path)

# Gri tonlamalı görüntüye dönüştür
# gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

#     # Histogram germe işlemini gerçekleştir
# stretched_image = histogram_stretching(gray_image)

#     # Orijinal görüntü, gerilmiş görüntü ve histogramları tek bir çerçeve içinde göster
# fig, axes = plt.subplots(2, 2, figsize=(15, 10))

#     # Orijinal görüntü
# axes[0, 0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
# axes[0, 0].set_title("Original Image")
# axes[0, 0].axis("off")

#     # Gerilmiş görüntü
# axes[0, 1].imshow(stretched_image, cmap="gray")
# axes[0, 1].set_title("Stretched Image")
# axes[0, 1].axis("off")

#     # Orijinal görüntü histogramı
# axes[1, 0].plot(calculate_histogram(gray_image), color="blue")
# axes[1, 0].set_title("Original Image Histogram")
# axes[1, 0].set_xlabel("Pixel Value")
# axes[1, 0].set_ylabel("Frequency")

#     # Gerilmiş görüntü histogramı
# axes[1, 1].plot(calculate_histogram(stretched_image), color="red")
# axes[1, 1].set_title("Stretched Image Histogram")
# axes[1, 1].set_xlabel("Pixel Value")
# axes[1, 1].set_ylabel("Frequency")

# plt.tight_layout()
# plt.show()
