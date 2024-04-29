import cv2
from PIL import Image

def convert_to_binary(image_path, threshold):
    image = Image.open(image_path)
    image = image.convert("L")  # Grayscale yap
    pixels = image.load()
    width, height = image.size

    binary_image = Image.new("1", (width, height))  # 1 bit per pixel (binary image)
    binary_pixels = binary_image.load()

    for y in range(height):
        for x in range(width):
            if pixels[x, y] > threshold:
                binary_pixels[x, y] = 255  # Beyaz (255) yap
            else:
                binary_pixels[x, y] = 0    # Siyah (0) yap

    return binary_image

image_path = r"C:\Users\yunusemrecoskun\Desktop\cat.jpg"  # Fotoğrafın dosya yolunu girin
threshold_value = 128  # Eşik değeri (0-255 arası)

binary_image = convert_to_binary(image_path, threshold_value)
binary_image.show()
cv2.waitKey(0)