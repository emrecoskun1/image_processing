from PIL import Image


def custom_cropp(image_path, x1, y1, x2, y2):
    try:
        # Görüntüyü yükle
        image = Image.open(image_path)

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

        # Kırpılmış görüntüyü göster
        cropped_image.show()

    except Exception as e:
        print("Hata:", e)


# Örnek kullanım
image_path = r"C:\Users\yunusemrecoskun\Desktop\vesikalik.jpeg"
x1, y1, x2, y2 = 100, 100, 600, 600  # Kırpma sınırları
custom_cropp(image_path, x1, y1, x2, y2)
