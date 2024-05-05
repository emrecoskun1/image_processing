import cv2
import numpy as np

def add_border(image, border_size, value=0):
    height, width = image.shape
    new_height = height + 2 * border_size
    new_width = width + 2 * border_size
    bordered_image = np.full((new_height, new_width), value, dtype=image.dtype)
    bordered_image[border_size:border_size+height, border_size:border_size+width] = image
    return bordered_image

def gaussian_kernel(kernel_size, sigma=1.0):
    kernel = [[0] * kernel_size[1] for _ in range(kernel_size[0])]
    m, n = kernel_size[0] // 2, kernel_size[1] // 2
    for x in range(-m, m + 1):
        for y in range(-n, n + 1):
            kernel[x + m][y + n] = (1 / (2 * np.pi * sigma ** 2)) * np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))
    return kernel / np.sum(kernel)

def convolution(image, kernel):
    height, width = image.shape
    kernel_size = len(kernel)
    pad = kernel_size // 2
    padded_image = add_border(image, pad)
    output = np.zeros_like(image)
    for i in range(height):
        for j in range(width):
            output[i, j] = np.sum(padded_image[i:i+kernel_size, j:j+kernel_size] * kernel)
    return output

def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, strength=1.5):
    kernel = gaussian_kernel(kernel_size, sigma)
    blurred = convolution(image, kernel)
    unsharp = image + strength * (image - blurred)
    unsharp = np.clip(unsharp, 0, 255)
    unsharp = unsharp.astype(np.uint8)
    return unsharp


image_path = "/Users/sevvalgencel/Desktop/X/ornek.jpg"

# Fotoğrafı yükle
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Unsharp maskesi filtresini uygula
filtered_image = unsharp_mask(image, kernel_size=(3, 3), sigma=1.0, strength=1.5)

cv2.imshow("Filtered Image", filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
