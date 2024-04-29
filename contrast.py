from PIL import Image

def adjust_contrast(image_path, ffactor):
    # Resmi aç
    image = Image.open(image_path)
    
    # Piksel değerlerini al
    pixels = image.load()
    width, height = image.size
    
    # Kontrastı arttır/azalt
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            new_r = int(ffactor * (r - 128) + 128)
            new_g = int(ffactor * (g - 128) + 128)
            new_b = int(ffactor * (b - 128) + 128)
            pixels[x, y] = (new_r, new_g, new_b)
    
    return image