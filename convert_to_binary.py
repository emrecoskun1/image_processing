from PIL import Image

def convert_to_binary(image_path, threshold):
    image = Image.open(image_path)
    image = image.convert("L")  
    pixels = image.load()
    width, height = image.size

    binary_image = Image.new("1", (width, height))
    binary_pixels = binary_image.load()

    for y in range(height):
        for x in range(width):
            if pixels[x, y] > threshold:
                binary_pixels[x, y] = 255  
            else:
                binary_pixels[x, y] = 0    
    return binary_image
