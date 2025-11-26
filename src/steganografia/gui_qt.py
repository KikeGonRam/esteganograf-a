import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QLineEdit, QMessageBox, QProgressBar
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import numpy as np
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))
from src.steganografia.image import ImageSteganography

class SteganoQt(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Esteganografía Avanzada (PyQt5)')
        self.setMinimumSize(500, 400)
        self.image_path = None
        self.file_to_hide = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.img_label = QLabel('Vista previa de imagen')
        self.img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.img_label)

        btns = QHBoxLayout()
        self.btn_load_img = QPushButton('Cargar Imagen')
        self.btn_load_img.clicked.connect(self.load_image)
        btns.addWidget(self.btn_load_img)

        self.btn_load_file = QPushButton('Seleccionar Archivo a Ocultar')
        self.btn_load_file.clicked.connect(self.load_file)
        btns.addWidget(self.btn_load_file)
        layout.addLayout(btns)

        self.password = QLineEdit()
        self.password.setPlaceholderText('Contraseña (opcional)')
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.btn_encode = QPushButton('Ocultar archivo en imagen')
        self.btn_encode.clicked.connect(self.encode_file)
        layout.addWidget(self.btn_encode)

        self.btn_decode = QPushButton('Extraer archivo de imagen')
        self.btn_decode.clicked.connect(self.decode_file)
        layout.addWidget(self.btn_decode)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.setLayout(layout)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Seleccionar imagen', '', 'Imágenes (*.png *.jpg *.jpeg *.bmp)')
        if path:
            self.image_path = path
            pixmap = QPixmap(path)
            self.img_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Seleccionar archivo a ocultar')
        if path:
            self.file_to_hide = path
            QMessageBox.information(self, 'Archivo seleccionado', f'Se ocultará: {os.path.basename(path)}')

    def encode_file(self):
        if not self.image_path or not self.file_to_hide:
            QMessageBox.warning(self, 'Faltan datos', 'Carga una imagen y selecciona un archivo a ocultar.')
            return
        pwd = self.password.text() or None
        out_path, _ = QFileDialog.getSaveFileName(self, 'Guardar imagen con archivo oculto', '', 'PNG (*.png)')
        if not out_path:
            return
        try:
            with open(self.file_to_hide, 'rb') as f:
                file_bytes = f.read()
            # Codificar archivo a base64
            import base64
            file_b64 = base64.b64encode(file_bytes).decode('utf-8')
            # Añadir nombre y extensión del archivo y separador especial
            filename = os.path.basename(self.file_to_hide)
            payload = filename + '||' + file_b64
            ImageSteganography.encode(self.image_path, out_path, payload, password=pwd, is_binary=False)
            QMessageBox.information(self, 'Éxito', 'Archivo oculto en la imagen.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def decode_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Seleccionar imagen con archivo oculto', '', 'Imágenes (*.png *.jpg *.jpeg *.bmp)')
        if not path:
            return
        pwd = self.password.text() or None
        try:
            payload = ImageSteganography.decode(path, password=pwd, is_binary=False)
            # Extraer nombre y datos
            header_end = payload.find('||')
            if header_end == -1:
                raise Exception('No se encontró archivo oculto.')
            filename = payload[:header_end]
            file_b64 = payload[header_end+2:]
            import base64
            file_bytes = base64.b64decode(file_b64)
            save_path, _ = QFileDialog.getSaveFileName(self, 'Guardar archivo extraído', filename)
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(file_bytes)
                QMessageBox.information(self, 'Éxito', f'Archivo extraído: {os.path.basename(save_path)}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

def main():
    app = QApplication(sys.argv)
    window = SteganoQt()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
