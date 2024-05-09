import numpy as np
import cv2


def convert_rgb_to_cmyk(rgb_image):
    # RGB değerlerini 0-1 aralığına getirme
    r, g, b = (
        rgb_image[:, :, 0] / 255.0,
        rgb_image[:, :, 1] / 255.0,
        rgb_image[:, :, 2] / 255.0,
    )

    # CMYK dönüşümü
    k = 1 - np.maximum(np.maximum(r, g), b)
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)

    # CMYK değerlerini 0-255 aralığına getirme
    c = (c * 255).astype(np.uint8)
    m = (m * 255).astype(np.uint8)
    y = (y * 255).astype(np.uint8)
    k = (k * 255).astype(np.uint8)

    # Yeni CMYK görüntü oluşturma
    cmyk_image = np.zeros((rgb_image.shape[0], rgb_image.shape[1], 4), dtype=np.uint8)
    cmyk_image[:, :, 0] = c
    cmyk_image[:, :, 1] = m
    cmyk_image[:, :, 2] = y
    cmyk_image[:, :, 3] = k

    return cmyk_image


# Örnek kullanım
image_path = r"C:\Users\yunusemrecoskun\Desktop\vesikalik.jpg"  # Görüntü dosya yolu
image = cv2.imread(image_path)

# RGB'den CMYK'ya dönüştürme
cmyk_image = convert_rgb_to_cmyk(image)

# Dönüştürülmüş CMYK görüntüyü gösterme
cv2.imshow("CMYK Image", cmyk_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
