from PIL import Image


def prewitt_edge_detection(image_path):
    # Görüntüyü yükle
    image = Image.open(image_path)
    grayscale_image = image.convert("L")  # Görüntüyü gri tonlama çevir

    # Görüntüyü listeye dönüştür
    img_list = list(grayscale_image.getdata())
    width, height = grayscale_image.size
    img_array = [img_list[i * width : (i + 1) * width] for i in range(height)]

    # Prewitt operatörü çekirdeği
    kernel_x = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]

    kernel_y = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]

    # Kenarlar için filtre uygula
    gradient_x = convolution(img_array, kernel_x)
    gradient_y = convolution(img_array, kernel_y)

    # Kenar yoğunluğunu hesapla
    edge_intensity = [
        [(gradient_x[y][x] ** 2 + gradient_y[y][x] ** 2) ** 0.5 for x in range(width)]
        for y in range(height)
    ]

    # Kenar yoğunluğunu 0 ile 255 arasında normalize et
    max_intensity = max(max(row) for row in edge_intensity)
    edge_intensity = [
        [int(pixel * 255 / max_intensity) for pixel in row] for row in edge_intensity
    ]

    # Normalleştirilmiş kenar yoğunluğunu Image objesine dönüştür
    edge_image = Image.new("L", (width, height))
    edge_image.putdata([pixel for row in edge_intensity for pixel in row])

    return edge_image


def convolution(image, kernel):
    # Görüntünün boyutlarını al
    height, width = len(image), len(image[0])

    # Kernelin boyutlarını al
    k_height, k_width = len(kernel), len(kernel[0])

    pad_height, pad_width = k_height // 2, k_width // 2
    padded_image = (
        [[0] * (width + 2 * pad_width) for _ in range(pad_height)]
        + image
        + [[0] * (width + 2 * pad_width) for _ in range(pad_height)]
    )
    padded_image = [[0] * pad_width + row + [0] * pad_width for row in padded_image]

    # Çıktı dizisını oluştur
    output = [[0] * width for _ in range(height)]

    # Kerneli ters çevir
    kernel = [row[::-1] for row in kernel[::-1]]

    # Konvolüsyon işlemi
    for y in range(height):
        for x in range(width):
            output[y][x] = sum(
                padded_image[y + i][x + j] * kernel[i][j]
                for i in range(k_height)
                for j in range(k_width)
            )

    return output
