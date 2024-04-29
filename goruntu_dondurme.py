from PIL import Image
import math

def rotate_image(image_path, angle):
    # Resmi aç
    image = Image.open(image_path)
    
    # Görüntü boyutlarını al
    width, height = image.size
    
    # Döndürülmüş görüntü için yeni boyutları hesapla
    new_width = int(width * abs(math.cos(math.radians(angle))) + height * abs(math.sin(math.radians(angle))))
    new_height = int(width * abs(math.sin(math.radians(angle))) + height * abs(math.cos(math.radians(angle))))
    
    # Döndürülmüş görüntüyü oluştur ve arka planı beyaz yap
    rotated_image = Image.new("RGB", (new_width, new_height), color="white")
    pixels_rotated = rotated_image.load()
    pixels_original = image.load()
    
    # Döndürülmüş görüntüyü oluştur
    for y in range(new_height):
        for x in range(new_width):
            # Döndürülen pikselin orijinal konumunu hesapla
            original_x = int((x - new_width / 2) * math.cos(math.radians(angle)) - (y - new_height / 2) * math.sin(math.radians(angle)) + width / 2)
            original_y = int((x - new_width / 2) * math.sin(math.radians(angle)) + (y - new_height / 2) * math.cos(math.radians(angle)) + height / 2)
            
            # Eğer orijinal piksel görüntünün içindeyse, döndürülmüş görüntüye ekle
            if 0 <= original_x < width and 0 <= original_y < height:
                pixels_rotated[x, y] = pixels_original[original_x, original_y]
    
    return rotated_image

# Görüntüyü döndürmek için dosya yolu
image_path = r"C:\Users\yunusemrecoskun\Desktop\cat.jpg"

# Kaç derece döndüreceğimizi dışarıdan al
angle = float(input("Kaç derece döndürmek istiyorsunuz: "))

# Görüntüyü döndür
rotated_image = rotate_image(image_path, angle)

# Döndürülmüş görüntüyü göster
rotated_image.show()
