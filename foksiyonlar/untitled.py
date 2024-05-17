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
from histogram_germe import histogram_stretching, calculate_histogram
from tek_esikleme import threshold
from renk_uzayi_hsv import convert_rgb_to_hsv
from arithmetic_operations_merge import merge_images, divide_images
from morfolojik_islemler import *
from salt_pepper_mean_median import *


class ImageProcessingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Görüntü İşleme Uygulaması")
        self.setGeometry(100, 100, 400, 400)

        self.resolution_label = QLabel(self)
        self.resolution_label2 = QLabel(self)  # QLabel öğesinin oluşturulması
        self.resolution_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.resolution_label.setStyleSheet(
            "font-weight: bold; font-size: 9px; color: red;"
        )
        self.resolution_label2.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.resolution_label2.setStyleSheet(
            "font-weight: bold; font-size: 9px; color: red;"
        )

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label2 = QLabel(self)
        self.image_label2.setAlignment(Qt.AlignCenter)

        self.select_button = QPushButton("Dosya Seç", self)
        self.select_button.clicked.connect(self.select_image)

        self.select_button2 = QPushButton("Dosya Seç (Görüntü 2)", self)
        self.select_button2.hide()
        self.select_button2.clicked.connect(self.select_image2)

        self.parameter_label_contrast = QLabel("Kontrast değerini giriniz :", self)
        self.parameter_label_contrast.hide()
        self.parameter_input_contrast = QLineEdit(self)
        self.parameter_input_contrast.hide()

        self.parameter_label_angel = QLabel(
            "Açı (saat yönünün tersine döndürür):", self
        )
        self.parameter_label_angel.hide()
        self.parameter_input_angel = QLineEdit(self)
        self.parameter_input_angel.hide()

        self.parameter_label_zoom = QLabel("Yaklaştırma faktörünü giriniz : ", self)
        self.parameter_label_zoom.hide()
        self.parameter_input_zoom = QLineEdit(self)
        self.parameter_input_zoom.hide()

        self.parameter_label_threshold = QLabel("Eşik değerini giriniz :", self)
        self.parameter_label_threshold.hide()
        self.parameter_input_threshold = QLineEdit(self)
        self.parameter_input_threshold.hide()

        self.parameter_label_density = QLabel(
            "Gürültü Seviyesini giriniz (1-'Girilen değer ' şeklinde hesaplanıyor.(0,01 vs.)):"
        )
        self.parameter_label_density.hide()
        self.parameter_input_density = QLineEdit(self)
        self.parameter_input_density.hide()

        self.parameter_label_filter = QLabel(
            "Filtre boyutunu giriniz(3,5 gibi 5 girdiğinizde 5*5 matris oluşturmuş olursunuz.) :"
        )
        self.parameter_label_filter.hide()
        self.parameter_input_filter = QLineEdit(self)
        self.parameter_input_filter.hide()

        self.parameter_label_crop = QLabel(
            "Kırpmak için x1,x2,y1,y2 değerlerini giriniz(Bu değerler x2-x1,y2-y1 şeklinde hesaplanıyor.) ",
            self,
        )
        self.parameter_label_crop.hide()

        self.parameter_input_crop = QLineEdit(self)
        self.parameter_input_crop.hide()

        self.process_button = QPushButton("Görüntüyü İşle", self)
        self.process_button.clicked.connect(self.process_image)

        # Combobox a fonskiyonları ekleme kısmı.
        self.function_selector = QComboBox(self)
        self.function_selector.addItem("Binary Dönüşüm")
        self.function_selector.addItem("Gri Dönüşüm")
        self.function_selector.addItem("Fotoğraf Döndürme")
        self.function_selector.addItem("Kontrast Arttırma/Azaltma")
        self.function_selector.addItem("Yakınlaştırma ve Uzaklaştırma")
        self.function_selector.addItem("Kenar Bulma (Prewitt)")
        self.function_selector.addItem("Fotoğraf Kırpma")
        self.function_selector.addItem("Konvolüsyon İşlemi(Mean Filtresi)")
        self.function_selector.addItem("Unsharp Filtresi")
        self.function_selector.addItem("Histogram Germe")
        self.function_selector.addItem("Tek Eşikleme")
        self.function_selector.addItem("RGB den HSV renk uzayına dönüşüm")
        self.function_selector.addItem("Aritmetik İşlemler(Ekleme, Bölme)")
        self.function_selector.addItem(
            "Morfolojik İşlemler(Genişleme,Aşınma,Açma,Kapama)"
        )
        self.function_selector.addItem(
            "Gürültü ekleme(Salt&Pepper) ve Filtre ile temizleme(Mean Median)"
        )
        self.function_selector.currentIndexChanged.connect(self.show_parameter_input)

        layout = QVBoxLayout()
        layout.addWidget(self.select_button)
        layout.addWidget(self.select_button2)
        layout.addWidget(self.parameter_label_angel)
        layout.addWidget(self.parameter_input_angel)
        layout.addWidget(self.parameter_label_contrast)
        layout.addWidget(self.parameter_input_contrast)
        layout.addWidget(self.parameter_label_zoom)
        layout.addWidget(self.parameter_input_zoom)
        layout.addWidget(self.parameter_label_crop)
        layout.addWidget(self.parameter_input_crop)
        layout.addWidget(self.parameter_label_threshold)
        layout.addWidget(self.parameter_input_threshold)
        layout.addWidget(self.parameter_label_density)
        layout.addWidget(self.parameter_input_density)
        layout.addWidget(self.parameter_label_filter)
        layout.addWidget(self.parameter_input_filter)
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.resolution_label2)
        layout.addWidget(self.image_label)
        layout.addWidget(self.image_label2)
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

            image = QImage(file_name)

            width = image.width()
            height = image.height()

            resolution_text = f"Çözünürlük: {width}x{height}"
            self.resolution_label.setText(resolution_text)

    def select_image2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name2, _ = QFileDialog.getOpenFileName(
            self,
            "Görüntü Seç",
            "",
            "Resim Dosyaları (*.jpg *.png *.tif)",
            options=options,
        )
        if file_name2:
            pixmap = QPixmap(file_name2)
            self.image_label2.setPixmap(pixmap.scaledToWidth(300))
            self.image_path2 = file_name2

            # Resmi yükle
            image = QImage(file_name2)

            width = image.width()
            height = image.height()

            resolution_text2 = f"2. Fotografın Çözünürlük: {width}x{height}"
            self.resolution_label2.setText(resolution_text2)

    def process_image(self):
        if not hasattr(self, "image_path"):
            QMessageBox.warning(self, "Uyarı", "Lütfen önce fotoğraf seçimi yapın.")
            return

        selected_function = self.function_selector.currentText()
        if selected_function == "Binary Dönüşüm":
            threshold_value = 128
            binary_image = convert_to_binary(self.image_path, threshold_value)
            binary_image.show()
        elif selected_function == "Gri Dönüşüm":
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
        # density gürültü seviyesini temsil ediyor
        elif (
            selected_function
            == "Gürültü ekleme(Salt&Pepper) ve Filtre ile temizleme(Mean Median)"
        ):
            density_text = self.parameter_input_density.text()
            density = float(density_text) if density_text else 0.01
            filter_text = self.parameter_input_filter.text()
            filter_size = int(filter_text) if filter_text else 0

            gray_lena = cv2.imread(self.image_path, 0)

            # add salt and paper (0.01 is a proper parameter)
            noise_lena = SaltAndPaper(gray_lena, density)

            #  3x3 mean görüntü
            # mean_3x3_lena = MeanFilter(noise_lena, 9)

            # 3x3 median görüntü
            # median_3x3_lena = MedianFilter(noise_lena, 9)

            mean_5x5_lena = MeanFilter(noise_lena, filter_size)

            # use 5x5 median filter
            median_5x5_lena = MedianFilter(noise_lena, filter_size)

            fig = plt.figure()
            fig.set_figheight(10)
            fig.set_figwidth(8)

            # display the oringinal image
            fig.add_subplot(2, 2, 1)
            plt.title("Original Image")
            plt.imshow(gray_lena, cmap="gray")

            # display the salt and paper image
            fig.add_subplot(2, 2, 2)
            plt.title("Adding Salt & Paper Image")
            plt.imshow(noise_lena, cmap="gray")

            # # display 3x3 mean filter
            # fig.add_subplot(3, 2, 3)
            # plt.title("3x3 Mean Filter")
            # plt.imshow(mean_3x3_lena, cmap="gray")

            # # display 3x3 median filter
            # fig.add_subplot(3, 2, 4)
            # plt.title("3x3 Median Filter")
            # plt.imshow(median_3x3_lena, cmap="gray")

            # display 5x5 median filter
            fig.add_subplot(2, 2, 3)
            plt.title("Mean Filter")
            plt.imshow(mean_5x5_lena, cmap="gray")

            # display 5x5 median filter
            fig.add_subplot(2, 2, 4)
            plt.title("Median Filter")
            plt.imshow(median_5x5_lena, cmap="gray")

            plt.show()
        elif selected_function == "RGB den HSV renk uzayına dönüşüm":
            image = cv2.imread(self.image_path)
            hsv_image = convert_rgb_to_hsv(image)
            cv2.imshow("HSV Image", hsv_image)
        elif selected_function == ("Morfolojik İşlemler(Genişleme,Aşınma,Açma,Kapama)"):
            image = cv2.imread(self.image_path)
            kernel = np.ones((3, 3), np.uint8)
            # Orijinal görüntüyü yükle

            # Orijinal görüntüyü ekrana yazdır
            plt.figure(figsize=(10, 6))
            plt.subplot(1, len(operations) + 1, 1)
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.title("Orijinal")
            plt.axis("off")

            # Tüm işlemleri uygula ve göster
            for idx, (operation_name, operation_func) in enumerate(operations):
                processed_image = operation_func(image, kernel)
                plt.subplot(1, len(operations) + 1, idx + 2)
                plt.imshow(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
                plt.title(operation_name)
                plt.axis("off")

            plt.show()
        elif selected_function == "Aritmetik İşlemler(Ekleme, Bölme)":
            image1_path = self.image_path
            image2_path = self.image_path2
            result_image_merge = merge_images(image1_path, image2_path)
            result_image_divide = divide_images(image1_path, image2_path)
            if result_image_merge is not None:
                cv2.imshow("Divide İmage", result_image_divide)
                cv2.imshow("Merge Image", result_image_merge)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        elif selected_function == "Tek Eşikleme":
            # Eşik değerini kullanıcıdan alma
            threshold_value_text = self.parameter_input_threshold.text()

            # Eşik değerinin boş olup olmadığını kontrol etme
            if not threshold_value_text:
                QMessageBox.warning(self, "Uyarı", "Lütfen bir eşik değeri girin.")
                return

            # Eşik değerini tam sayıya dönüştürme
            try:
                threshold_value = int(threshold_value_text)
            except ValueError:
                QMessageBox.warning(
                    self, "Uyarı", "Lütfen geçerli bir tam sayı eşik değeri girin."
                )
                return

            # Görüntüyü yükleme
            image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

            # Eşikleme işlemini uygulama
            thresholded_image = threshold(image, threshold_value)

            # Eşiklenmiş görüntüyü gösterme
            plt.imshow(thresholded_image, cmap="gray")
            plt.title("Eşiklenmiş Görüntü (Eşik Değeri = {})".format(threshold_value))
            plt.axis("off")
            plt.show()
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
            self.image_label2.hide()
            original_image = cv2.imread(self.image_path)
            # Ortalama filtre için kernel tanımlama
            kernel = np.ones((3, 3), np.float32) / 9

            gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
            noisy_image = gray_image + np.random.normal(0, 25, gray_image.shape).astype(
                np.uint8
            )

            mean_filtered_image = convolution(noisy_image, kernel)

            fig, axs = plt.subplots(1, 4, figsize=(20, 5))

            axs[0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
            axs[0].set_title("Orijinal Resim")

            axs[1].imshow(gray_image, cmap="gray")
            axs[1].set_title("Gri Tonlamalı Resim")

            axs[2].imshow(noisy_image, cmap="gray")
            axs[2].set_title("Gürültülü Resim")

            axs[3].imshow(mean_filtered_image, cmap="gray")
            axs[3].set_title("Ortalama Filtre Uygulanmış Resim")

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
        self.parameter_input_threshold.hide()
        self.parameter_label_threshold.hide()
        self.parameter_input_density.hide()
        self.parameter_label_density.hide()
        self.parameter_input_filter.hide()
        self.parameter_label_filter.hide()
        self.select_button2.hide()
        self.resolution_label2.hide()

        if selected_function == "Fotoğraf Döndürme":
            self.parameter_label_angel.show()
            self.parameter_input_angel.show()
            self.image_label2.hide()
        if selected_function == "Binary Dönüşüm":
            self.image_label2.hide()
        elif selected_function == "Unsharp Filtresi":
            self.image_label2.hide()
        elif selected_function == "Kontrast Arttırma/Azaltma":
            self.parameter_label_contrast.show()
            self.parameter_input_contrast.show()
            self.image_label2.hide()
        elif selected_function == "Yakınlaştırma ve Uzaklaştırma":
            self.parameter_input_zoom.show()
            self.parameter_label_zoom.show()
            self.image_label2.hide()
        elif selected_function == "Fotoğraf Kırpma":
            self.parameter_input_crop.show()
            self.parameter_label_crop.show()
            self.image_label2.hide()
        elif selected_function == "Kenar Bulma (Prewitt)":
            self.image_label2.hide()
        elif selected_function == "Tek Eşikleme":
            self.parameter_input_threshold.show()
            self.parameter_label_threshold.show()
            self.image_label2.hide()
        elif selected_function == "Aritmetik İşlemler(Ekleme, Bölme)":
            self.image_label2.show()
            self.select_button2.show()
            self.resolution_label2.show()
        elif selected_function == "Morfolojik İşlemler(Genişleme,Aşınma,Açma,Kapama)":
            self.image_label2.hide()
        elif (
            selected_function
            == "Gürültü ekleme(Salt&Pepper) ve Filtre ile temizleme(Mean Median)"
        ):
            self.parameter_label_filter.show()
            self.parameter_input_filter.show()
            self.parameter_label_density.show()
            self.parameter_input_density.show()
            self.image_label2.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())
