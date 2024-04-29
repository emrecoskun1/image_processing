from PIL import Image

def zoom_image(image_path, scale_factor):
    # Resmi aç
    image = Image.open(image_path)
    
    # Görüntü boyutlarını al
    width, height = image.size
    
    # Yeni boyutları hesapla
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    # Yeniden boyutlandırılmış görüntüyü oluştur
    zoomed_image = image.resize((new_width, new_height))
    
    return zoomed_image