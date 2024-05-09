import cv2
import numpy as np


def divide_images(image1_path, image2_path):
    # İlk resmi oku
    image1 = cv2.imread(image1_path)
    # İkinci resmi oku
    image2 = cv2.imread(image2_path)

    # İki resmin boyutlarını al
    height1, width1, _ = image1.shape
    height2, width2, _ = image2.shape

    # İki resmin en büyük boyutunu bul
    max_width = max(width1, width2)
    max_height = max(height1, height2)

    # İlk resmi yeniden boyutlandır
    resized_image1 = np.zeros((max_height, max_width, 3), dtype=np.uint8)
    resized_image1[:height1, :width1, :] = image1

    # İkinci resmi yeniden boyutlandır
    resized_image2 = np.zeros((max_height, max_width, 3), dtype=np.uint8)
    resized_image2[:height2, :width2, :] = image2

    # İki resmi birbirine bölecek işlemi gerçekleştir
    divided_image = np.zeros((max_height, max_width, 3), dtype=np.float64)
    for i in range(max_height):
        for j in range(max_width):
            # İkinci resmin piksel değeri sıfırdan farklı ise işlem yap
            if np.any(resized_image2[i, j] != 0):
                divided_image[i, j] = np.divide(
                    resized_image1[i, j],
                    resized_image2[i, j],
                    out=np.zeros(3, dtype=np.float64),
                    where=resized_image2[i, j] != 0,
                )

    return divided_image.astype(np.uint8)


# Kullanım örneği
image1_path = r"C:\Users\yunusemrecoskun\Desktop\cat.jpg"
image2_path = r"C:\Users\yunusemrecoskun\Desktop\mssql.jpg"
result_image = divide_images(image1_path, image2_path)
if result_image is not None:
    cv2.imshow("Divided Image", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
