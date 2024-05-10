import cv2
import numpy as np
import matplotlib.pyplot as plt


def genisleme(image, kernel):
    # Görüntü üzerinde genişleme işlemi uygulama
    output = np.zeros_like(image)
    k_height, k_width = kernel.shape
    k_center_x, k_center_y = k_width // 2, k_height // 2

    for channel in range(image.shape[2]):
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                max_value = 0
                for m in range(k_height):
                    for n in range(k_width):
                        if kernel[m, n] == 1:
                            x = i + (m - k_center_y)
                            y = j + (n - k_center_x)
                            if (
                                x >= 0
                                and x < image.shape[0]
                                and y >= 0
                                and y < image.shape[1]
                            ):
                                if image[x, y, channel] > max_value:
                                    max_value = image[x, y, channel]
                output[i, j, channel] = max_value

    return output


def asinma(image, kernel):
    # Görüntü üzerinde aşınma işlemi uygulama
    output = np.zeros_like(image)
    k_height, k_width = kernel.shape
    k_center_x, k_center_y = k_width // 2, k_height // 2

    for channel in range(image.shape[2]):
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                min_value = 255
                for m in range(k_height):
                    for n in range(k_width):
                        if kernel[m, n] == 1:
                            x = i + (m - k_center_y)
                            y = j + (n - k_center_x)
                            if (
                                x >= 0
                                and x < image.shape[0]
                                and y >= 0
                                and y < image.shape[1]
                            ):
                                if image[x, y, channel] < min_value:
                                    min_value = image[x, y, channel]
                output[i, j, channel] = min_value

    return output


def acma(image, kernel):
    # Görüntü üzerinde açma işlemi uygulama (genişleme + aşınma)
    temp = genisleme(image, kernel)
    output = asinma(temp, kernel)
    return output


def kapama(image, kernel):
    # Görüntü üzerinde kapama işlemi uygulama (aşınma + genişleme)
    temp = asinma(image, kernel)
    output = genisleme(temp, kernel)
    return output


# Örnek kullanım
image_path = "/Users/sevvalgencel/Desktop/X/ornek.jpg"
kernel = np.ones((3, 3), np.uint8)

# Her bir işlem için işlem adını ve işlem fonksiyonunu belirterek işlemi uygula ve göster
operations = [
    ("Genisleme", genisleme),
    ("Asinma", asinma),
    ("Acma", acma),
    ("Kapama", kapama),
]

# # Orijinal görüntüyü yükle
# original_image = cv2.imread(image_path)

# # Orijinal görüntüyü ekrana yazdır
# plt.figure(figsize=(10, 6))
# plt.subplot(1, len(operations) + 1, 1)
# plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
# plt.title("Orijinal")
# plt.axis('off')

# # Tüm işlemleri uygula ve göster
# for idx, (operation_name, operation_func) in enumerate(operations):
#     processed_image = operation_func(original_image, kernel)
#     plt.subplot(1, len(operations) + 1, idx + 2)
#     plt.imshow(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
#     plt.title(operation_name)
#     plt.axis('off')

# plt.show()
