import cv2
import numpy as np

def unsharp_mask(image_path, kernel_size=(5, 5), sigma=1.0, strength=1.5):
    # Görüntüyü yükle
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Gauss filtresi kerneli oluştur
    kernel = np.zeros(kernel_size)
    m, n = [(ss - 1) / 2 for ss in kernel_size]
    for x in range(-int(m), int(m) + 1):
        for y in range(-int(n), int(n) + 1):
            kernel[int(m) + x, int(n) + y] = (1 / (2 * np.pi * sigma ** 2)) * np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))
    kernel = kernel / kernel.sum()
    
    # Gauss filtresini uygula
    blurred = cv2.filter2D(image, -1, kernel)
    
    # Kenarları vurgulamak için unsharp mask oluştur
    unsharp = image + strength * (image - blurred)
    
    # Sınırları kontrol et
    unsharp = np.clip(unsharp, 0, 255)
    unsharp = unsharp.astype(np.uint8)
    
    return unsharp

# Örnek olarak unsharp mask filtresini uygula
image_path = "example.jpg"
filtered_image = unsharp_mask(image_path, kernel_size=(5, 5), sigma=1.0, strength=1.5)

# Filtrelenmiş görüntüyü göster
cv2.imshow("Filtered Image", filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
