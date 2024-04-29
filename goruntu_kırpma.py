from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

def custom_crop(image_path, x1, y1, x2, y2):
    try:
        # Görüntüyü yükle
        image = Image.open(image_path)
        
        # Görüntüyü RGB modunda matrise dönüştür
        img_array = image.convert("RGB")
        img_array = img_array.load()
        

        # Görüntünün boyutlarını al
        width, height = image.size

        # Genişlik ve yükseklik değerlerini bir metin dizesine dönüştür
        message = f"Görüntünün boyutları: Genişlik = {width}, Yükseklik = {height}"

        # MessageBox ile mesajı göster
        QMessageBox.warning(None, "Boyut Bilgisi", message)
        
        
        # Belirtilen kırpma sınırlarını kontrol et
        if x1 < 0 or y1 < 0 or x2 > width or y2 > height or x2 <= x1 or y2 <= y1:
            raise ValueError("Geçersiz kırpma sınırları. Lütfen sınırları kontrol edin.")
        
        # Kırpılan bölgeyi içeren yeni bir matris oluştur
        cropped_img_array = []
        for y in range(y1, y2):
            row = []
            for x in range(x1, x2):
                row.append(img_array[x, y])
            cropped_img_array.append(row)
        
        # Yeni matrisi PIL Image nesnesine dönüştür
        cropped_image = Image.new("RGB", (x2 - x1, y2 - y1))
        cropped_image.putdata([pixel for row in cropped_img_array for pixel in row])
        
        # Kırpılan bölgeyi JPEG formatında kaydet
        cropped_image.show()

    
    except Exception as e:
        print("Hata:", e)

# Örnek kullanım
image_path = r"C:\Users\yunusemrecoskun\Desktop\cat.jpg"
x1, y1, x2, y2 = 0, 0, 200, 240  # Kırpma sınırları
custom_crop(image_path, x1, y1, x2, y2)



