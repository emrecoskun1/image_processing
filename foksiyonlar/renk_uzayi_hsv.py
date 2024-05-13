import numpy as np
import cv2


def convert_rgb_to_hsv(rgb_image):
    # RGB değerlerini ayrıştırma
    r, g, b = rgb_image[:, :, 0], rgb_image[:, :, 1], rgb_image[:, :, 2]

    # Normalleştirme
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    # Hesaplama
    cmax = np.maximum(np.maximum(r, g), b)
    cmin = np.minimum(np.minimum(r, g), b)
    diff = cmax - cmin

    # Hue hesaplama
    h = np.zeros_like(cmax)
    h[np.where(cmax == cmin)] = 0
    h[np.where(cmax == r)] = (60 * ((g - b) / diff) % 6)[np.where(cmax == r)]
    h[np.where(cmax == g)] = (60 * ((b - r) / diff) + 2)[np.where(cmax == g)]
    h[np.where(cmax == b)] = (60 * ((r - g) / diff) + 4)[np.where(cmax == b)]

    # Value hesaplama
    v = cmax

    # Saturation hesaplama
    s = np.zeros_like(cmax)
    s[np.where(cmax != 0)] = (diff / cmax)[np.where(cmax != 0)]

    # Normalleştirme
    h = (h / 360.0) * 179.0
    s = s * 255.0
    v = v * 255.0

    # HSV görüntü oluşturma
    hsv_image = np.zeros_like(rgb_image)
    hsv_image[:, :, 0] = h
    hsv_image[:, :, 1] = s
    hsv_image[:, :, 2] = v

    return hsv_image.astype(np.uint8)


# Örnek kullanım
# image_path = r"C:\Users\yunusemrecoskun\Desktop\cat.jpg"
# image = cv2.imread(image_path)
# hsv_image = convert_rgb_to_hsv(image)

# # HSV görüntüyü gösterme
# cv2.imshow("HSV Image", hsv_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
