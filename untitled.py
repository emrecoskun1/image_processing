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
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
from rotate_image import rotate_image
from convert_gray import convert_gray
from convert_to_binary import convert_to_binary
from contrast import adjust_contrast
from zoomin_zoomout import zoom_image
from prewitt_edge_detection import prewitt_edge_detection
from imagecrop import custom_crop


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
