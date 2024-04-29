from PIL import Image

def rgb_to_cmyk(image_path):
    # RGB görüntüyü aç
    rgb_image = Image.open(image_path)
    
    # CMYK için boş bir görüntü oluştur
    cmyk_image = Image.new('CMYK', rgb_image.size)
    
    # RGB görüntüyü CMYK'ya dönüştür
    for x in range(rgb_image.width):
        for y in range(rgb_image.height):
            # RGB piksel değerlerini al
            r, g, b = rgb_image.getpixel((x, y))
            
            # CMYK'ya dönüştürme işlemi
            c = 1 - r / 255.0
            m = 1 - g / 255.0
            y_ = 1 - b / 255.0
            k = min(c, m, y_)
            if k == 1:
                c = m = y_ = 0
            else:
                c = (c - k) / (1 - k)
                m = (m - k) / (1 - k)
                y_ = (y_ - k) / (1 - k)
            
            # CMYK piksel değerlerini ayarla
            cmyk_image.putpixel((x, y), (int(c * 255), int(m * 255), int(y_ * 255), int(k * 255)))
    
    return cmyk_image

# Örnek kullanım
rgb_image_path = r"C:\Users\yunusemrecoskun\Desktop\vesikalik.jpeg"
cmyk_image = rgb_to_cmyk(rgb_image_path)
cmyk_image.show("dönüştürülmüş_cmyk_görüntü.tif")





