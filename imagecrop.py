from PIL import Image

def custom_crop(image_path, x1, y1, x2, y2):
    try:
        
        # Görüntüyü yükle
        image = Image.open(image_path)
        width, height = image.size
        
        # Görüntüyü RGB modunda yükle
        img_array = image.convert("RGB")
        img_array = img_array.load()
        
        # Kırpılmış görüntüyü içeren yeni bir matris oluştur
        cropped_img_array = []
        for y in range(y1, y2):
            row = []
            for x in range(x1, x2):
                row.append(img_array[x, y])
            cropped_img_array.append(row)
        
        # Yeni matrisi PIL Image nesnesine dönüştür
        cropped_image = Image.new("RGB", (x2 - x1, y2 - y1))
        cropped_image.putdata([pixel for row in cropped_img_array for pixel in row])
        
        return cropped_image
    
    except Exception as e:
        print("Hata:", e)

