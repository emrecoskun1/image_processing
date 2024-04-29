import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import cv2
from rotate_image import rotate_image
from convert_gray import convert_gray
from convert_to_binary import convert_to_binary
from contrast import adjust_contrast
from zoomin_zoomout import zoom_image
from prewitt_edge_detection import prewitt_edge_detection



class ImageProcessingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Görüntü İşleme Uygulaması")
        self.setGeometry(100, 100, 400, 400)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.select_button = QPushButton("Dosya Seç", self)
        self.select_button.clicked.connect(self.select_image)

        self.parameter_label2 = QLabel("Kontrast değerini giriniz :",self)
        self.parameter_label2.hide()

        self.parameter_input2 = QLineEdit(self)
        self.parameter_input2.hide()

        self.parameter_label = QLabel("Açı (sadece döndürme için):", self)
        self.parameter_label.hide()

        self.parameter_input = QLineEdit(self)
        self.parameter_input.hide()

        self.parameter_label3 = QLabel("Yaklaştırma faktörünü giriniz : ", self)
        self.parameter_label3.hide()

        self.parameter_input3= QLineEdit(self)
        self.parameter_input3.hide()

        self.process_button = QPushButton("Görüntüyü İşle", self)
        self.process_button.clicked.connect(self.process_image)

        self.function_selector = QComboBox(self)
        self.function_selector.addItem("Binary Dönüşüm")
        self.function_selector.addItem("Grayscale Dönüşüm")
        self.function_selector.addItem("Fotoğraf Döndürme")
        self.function_selector.addItem("Kontrast Arttırma/Azaltma")
        self.function_selector.addItem("Yakınlaştırma ve Uzaklaştırma")
        self.function_selector.addItem("Kenar Bulma (Prewitt)")
        self.function_selector.currentIndexChanged.connect(self.show_parameter_input)

        layout = QVBoxLayout()
        layout.addWidget(self.select_button)
        layout.addWidget(self.parameter_label)
        layout.addWidget(self.parameter_input)
        layout.addWidget(self.parameter_label2)
        layout.addWidget(self.parameter_input2)
        layout.addWidget(self.parameter_label3)
        layout.addWidget(self.parameter_input3)
        layout.addWidget(self.image_label)
        layout.addWidget(self.function_selector)
        layout.addWidget(self.process_button)

        self.setLayout(layout)

    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Görüntü Seç", "", "Resim Dosyaları (*.jpg *.png *.tif)", options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaledToWidth(300))
            self.image_path = file_name

    def process_image(self):
        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self,"Uyarı", "Lütfen önce fotoğraf seçimi yapın.")
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
            angle = float(self.parameter_input.text())
            rotated_image = rotate_image(self.image_path, angle)
            rotated_image.show()
        elif selected_function == "Kontrast Arttırma/Azaltma":
            factor= (self.parameter_input2.text())
            if factor =="":
                QMessageBox.warning(self,"Uyarı","Lütfen kontrast değerini giriniz.")
                return
            ffactor=float(factor)
            image = cv2.imread(self.image_path)
            image = adjust_contrast(self.image_path,ffactor)
            image.show()
        elif selected_function == "Kenar Bulma (Prewitt)":
            prewitt_image = prewitt_edge_detection(self.image_path)
            prewitt_image.show()
        elif selected_function == "Yakınlaştırma ve Uzaklaştırma":
            scale_factor = float(self.parameter_input3.text())
            if scale_factor <=0 :
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setText("Lütfen pozitif bir sayı girin.")
                msg.setWindowTitle("Hata")
                msg.exec_()
            else:
                zoomed_image = cv2.imread(self.image_path)
                zoomed_image = zoom_image(self.image_path,scale_factor)
                zoomed_image.show()


    def show_parameter_input(self):
        selected_function = self.function_selector.currentText()
        self.parameter_label.hide()
        self.parameter_input.hide()
        self.parameter_label2.hide()
        self.parameter_input2.hide()
        self.parameter_input3.hide()
        self.parameter_label3.hide()
        if selected_function == "Fotoğraf Döndürme":
            self.parameter_label.show()
            self.parameter_input.show()
        elif selected_function == "Kontrast Arttırma/Azaltma":
            self.parameter_label2.show()
            self.parameter_input2.show()
        elif selected_function == "Yakınlaştırma ve Uzaklaştırma":
            self.parameter_input3.show()
            self.parameter_label3.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())
