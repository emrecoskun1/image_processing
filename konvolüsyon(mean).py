import numpy as np
import cv2

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
            image_patch = image[i:i+kernel_height, j:j+kernel_width]
            # Konvolüsyon işlemi
            output[i, j] = np.mean(image_patch * kernel)
    
    return output

# Resmin yolunu belirle
image_path = r"C:\Users\yunusemrecoskun\Desktop\vesikalik.jpeg"  # Resmin yolunu buraya yazın

# Resmi yükle
original_image = cv2.imread(image_path)
gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

# Gürültü ekleyelim
noisy_image = gray_image + np.random.normal(0, 25, gray_image.shape).astype(np.uint8)

# Ortalama filtre için kernel tanımlayalım
kernel = np.ones((3,3), np.float32) / 9

# Ortalama filtre uygulayalım
mean_filtered_image = convolution(noisy_image, kernel)

# Orijinal, gri, gürültülü ve ortalama uygulanmış resimleri gösterelim
cv2.imshow("Orijinal Resim", original_image)
cv2.imshow("Gri Tonlamalı Resim", gray_image)
cv2.imshow("Gürültülü Resim", noisy_image)
cv2.imshow("Ortalama Filtre Uygulanmış Resim", mean_filtered_image.astype(np.uint8))

cv2.waitKey(0)
cv2.destroyAllWindows()

