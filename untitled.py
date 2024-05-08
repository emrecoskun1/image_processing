import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QLabel,
    QComboBox,
    QLineEdit,
)
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from rotate_image import rotate_image
from convert_gray import convert_gray
from convert_to_binary import convert_to_binary
from contrast import adjust_contrast
from zoomin_zoomout import zoom_image
from prewitt_edge_detection import prewitt_edge_detection
from imagecrop import custom_crop
from convolution import convolution
from filtre_unsharp import unsharp_mask
from histogram_germe import histogram_stretching
from histogram_germe import calculate_histogram


class ImageProcessingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Görüntü İşleme Uygulaması")
        self.setGeometry(100, 100, 400, 400)

        self.resolution_label = QLabel(self)  # QLabel öğesinin oluşturulması
        self.resolution_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.resolution_label.setStyleSheet(
            "font-weight: bold; font-size: 9px; color: red;"
        )  # Metnin stilinin ayarlanması

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.select_button = QPushButton("Dosya Seç", self)
        self.select_button.clicked.connect(self.select_image)

        self.parameter_label_contrast = QLabel("Kontrast değerini giriniz :", self)
        self.parameter_label_contrast.hide()

        self.parameter_input_contrast = QLineEdit(self)
        self.parameter_input_contrast.hide()

        self.parameter_label_angel = QLabel("Açı (sadece döndürme için):", self)
        self.parameter_label_angel.hide()

        self.parameter_input_angel = QLineEdit(self)
        self.parameter_input_angel.hide()

        self.parameter_label_zoom = QLabel("Yaklaştırma faktörünü giriniz : ", self)
        self.parameter_label_zoom.hide()

        self.parameter_input_zoom = QLineEdit(self)
        self.parameter_input_zoom.hide()

        self.parameter_label_crop = QLabel(
            "Kırpmak için x1,x2,y1,y2 değerlerini giriniz(Bu değerler x2-x1,y2-y1 şeklinde hesaplanıyor.) ",
            self,
        )
        self.parameter_label_crop.hide()

        self.parameter_input_crop = QLineEdit(self)
        self.parameter_input_crop.hide()

        self.process_button = QPushButton("Görüntüyü İşle", self)
        self.process_button.clicked.connect(self.process_image)

        self.function_selector = QComboBox(self)
        self.function_selector.addItem("Binary Dönüşüm")
        self.function_selector.addItem("Grayscale Dönüşüm")
        self.function_selector.addItem("Fotoğraf Döndürme")
        self.function_selector.addItem("Kontrast Arttırma/Azaltma")
        self.function_selector.addItem("Yakınlaştırma ve Uzaklaştırma")
        self.function_selector.addItem("Kenar Bulma (Prewitt)")
        self.function_selector.addItem("Fotoğraf Kırpma")
        self.function_selector.addItem("Konvolüsyon İşlemi(Mean Filtresi)")
        self.function_selector.addItem("Unsharp Filtresi")
        self.function_selector.addItem("Histogram Germe")
        self.function_selector.currentIndexChanged.connect(self.show_parameter_input)

        layout = QVBoxLayout()
        layout.addWidget(self.select_button)
        layout.addWidget(self.parameter_label_angel)
        layout.addWidget(self.parameter_input_angel)
        layout.addWidget(self.parameter_label_contrast)
        layout.addWidget(self.parameter_input_contrast)
        layout.addWidget(self.parameter_label_zoom)
        layout.addWidget(self.parameter_input_zoom)
        layout.addWidget(self.parameter_label_crop)
        layout.addWidget(self.parameter_input_crop)
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.function_selector)
        layout.addWidget(self.process_button)

        self.setLayout(layout)

    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Görüntü Seç",
            "",
            "Resim Dosyaları (*.jpg *.png *.tif)",
            options=options,
        )
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaledToWidth(300))
            self.image_path = file_name

            # Resmi yükle
            image = QImage(file_name)

            # Çözünürlüğü al
            width = image.width()
            height = image.height()

            # Çözünürlüğü ekrana yazdır
            resolution_text = f"Çözünürlük: {width}x{height}"
            self.resolution_label.setText(
                resolution_text
            )  # resolution_label adında bir QLabel öğesine yazdırın veya başka bir şekilde çözünürlüğü göstereceğiniz bir öğe varsa onu kullanın.

    def process_image(self):
        if not hasattr(self, "image_path"):
            QMessageBox.warning(self, "Uyarı", "Lütfen önce fotoğraf seçimi yapın.")
            return

        selected_function = self.function_selector.currentText()
        if selected_function == "Binary Dönüşüm":
            threshold_value = 128
            binary_image = convert_to_binary(self.image_path, threshold_value)
            binary_image.show()
        elif selected_function == "Grayscale Dönüşüm":
            image = cv2.imread(self.image_path)
            gray_image = convert_gray(image)
            cv2.imshow("Grayscale Image", gray_image)
            cv2.waitKey(0)
        elif selected_function == "Fotoğraf Döndürme":
            angle = float(self.parameter_input_angel.text())
            rotated_image = rotate_image(self.image_path, angle)
            rotated_image.show()
        elif selected_function == "Kontrast Arttırma/Azaltma":
            factor = self.parameter_input_contrast.text()
            if factor == "":
                QMessageBox.warning(self, "Uyarı", "Lütfen kontrast değerini giriniz.")
                return
            ffactor = float(factor)
            image = cv2.imread(self.image_path)
            image = adjust_contrast(self.image_path, ffactor)
            image.show()
        elif selected_function == "Kenar Bulma (Prewitt)":
            prewitt_image = prewitt_edge_detection(self.image_path)
            prewitt_image.show()
        elif selected_function == "Unsharp Filtresi":
            image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
            filtered_image = unsharp_mask(
                image, kernel_size=(3, 3), sigma=1.0, strength=1.5
            )
            cv2.imshow("Filtered Image", filtered_image)
        elif selected_function == "Histogram Germe":
            original_image = cv2.imread(self.image_path)
            gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
            # Histogram germe işlemini gerçekleştir
            stretched_image = histogram_stretching(gray_image)

            # Orijinal görüntü, gerilmiş görüntü ve histogramları tek bir çerçeve içinde göster
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))

            # Orijinal görüntü
            axes[0, 0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
            axes[0, 0].set_title("Original Image")
            axes[0, 0].axis("off")

            # Gerilmiş görüntü
            axes[0, 1].imshow(stretched_image, cmap="gray")
            axes[0, 1].set_title("Stretched Image")
            axes[0, 1].axis("off")

            # Orijinal görüntü histogramı
            axes[1, 0].plot(calculate_histogram(gray_image), color="blue")
            axes[1, 0].set_title("Original Image Histogram")
            axes[1, 0].set_xlabel("Pixel Value")
            axes[1, 0].set_ylabel("Frequency")

            # Gerilmiş görüntü histogramı
            axes[1, 1].plot(calculate_histogram(stretched_image), color="red")
            axes[1, 1].set_title("Stretched Image Histogram")
            axes[1, 1].set_xlabel("Pixel Value")
            axes[1, 1].set_ylabel("Frequency")

            plt.tight_layout()
            plt.show()

        elif selected_function == "Konvolüsyon İşlemi(Mean Filtresi)":
            original_image = cv2.imread(self.image_path)
            # Ortalama filtre için kernel tanımlayalım
            kernel = np.ones((3, 3), np.float32) / 9

            # Gürültülü resmi yükleyelim
            gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
            noisy_image = gray_image + np.random.normal(0, 25, gray_image.shape).astype(
                np.uint8
            )

            # Ortalama filtre uygulayalım
            mean_filtered_image = convolution(noisy_image, kernel)

            fig, axs = plt.subplots(1, 4, figsize=(20, 5))

            # Orijinal resmi göster
            axs[0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
            axs[0].set_title("Orijinal Resim")

            # Gri tonlamalı resmi göster
            axs[1].imshow(gray_image, cmap="gray")
            axs[1].set_title("Gri Tonlamalı Resim")

            # Gürültülü resmi göster
            axs[2].imshow(noisy_image, cmap="gray")
            axs[2].set_title("Gürültülü Resim")

            # Ortalama filtre uygulanmış resmi göster
            axs[3].imshow(mean_filtered_image, cmap="gray")
            axs[3].set_title("Ortalama Filtre Uygulanmış Resim")

            # Alt resimler arasındaki boşlukları sıkıştır
            plt.tight_layout()

            # Görüntüleri göster
            plt.show()
        elif selected_function == "Yakınlaştırma ve Uzaklaştırma":
            scale_factor = float(self.parameter_input_zoom.text())
            if scale_factor <= 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setText("Lütfen pozitif bir sayı girin.")
                msg.setWindowTitle("Hata")
                msg.exec_()
            else:
                zoomed_image = cv2.imread(self.image_path)
                zoomed_image = zoom_image(self.image_path, scale_factor)
                zoomed_image.show()
        elif selected_function == "Fotoğraf Kırpma":
            try:
                x1, y1, x2, y2 = map(int, self.parameter_input_crop.text().split(","))
                cropped_image = custom_crop(self.image_path, x1, y1, x2, y2)
                cropped_image.show()
                app.exec_()
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Uyarı",
                    "Lütfen dört tane tamsayı değeri girin (x1, y1, x2, y2).",
                )
        return

    def show_parameter_input(self):
        selected_function = self.function_selector.currentText()
        self.parameter_label_angel.hide()
        self.parameter_input_angel.hide()
        self.parameter_label_contrast.hide()
        self.parameter_input_contrast.hide()
        self.parameter_input_zoom.hide()
        self.parameter_label_zoom.hide()
        self.parameter_input_crop.hide()
        self.parameter_label_crop.hide()
        if selected_function == "Fotoğraf Döndürme":
            self.parameter_label_angel.show()
            self.parameter_input_angel.show()
        elif selected_function == "Kontrast Arttırma/Azaltma":
            self.parameter_label_contrast.show()
            self.parameter_input_contrast.show()
        elif selected_function == "Yakınlaştırma ve Uzaklaştırma":
            self.parameter_input_zoom.show()
            self.parameter_label_zoom.show()
        elif selected_function == "Fotoğraf Kırpma":
            self.parameter_input_crop.show()
            self.parameter_label_crop.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())
