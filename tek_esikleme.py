import cv2
import numpy as np
import matplotlib.pyplot as plt

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

# Görüntünün yüklenmesi
path = "/Users/sevvalgencel/Desktop/X/kedy.jpg"
image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

# Kullanıcıdan eşik değerini alma
threshold_value = int(input("Eşik değerini girin: "))

# Eşikleme işlemi
thresholded_image = threshold(image, threshold_value)

# Sonuçları görselleştirme
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(thresholded_image, cmap='gray')
plt.title('Thresholded Image (Threshold = {})'.format(threshold_value))
plt.axis('off')

plt.show()
