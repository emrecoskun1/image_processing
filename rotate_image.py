from PIL import Image
import math

def rotate_image(image_path, angle):
    image = Image.open(image_path)
    width, height = image.size
    new_width = int(width * abs(math.cos(math.radians(angle))) + height * abs(math.sin(math.radians(angle))))
    new_height = int(width * abs(math.sin(math.radians(angle))) + height * abs(math.cos(math.radians(angle))))
    rotated_image = Image.new("RGB", (new_width, new_height), color="white")
    pixels_rotated = rotated_image.load()
    pixels_original = image.load()
    
    for y in range(new_height):
        for x in range(new_width):
            original_x = int((x - new_width / 2) * math.cos(math.radians(angle)) - (y - new_height / 2) * math.sin(math.radians(angle)) + width / 2)
            original_y = int((x - new_width / 2) * math.sin(math.radians(angle)) + (y - new_height / 2) * math.cos(math.radians(angle)) + height / 2)
            if 0 <= original_x < width and 0 <= original_y < height:
                pixels_rotated[x, y] = pixels_original[original_x, original_y]
    return rotated_image
