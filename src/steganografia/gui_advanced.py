import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QFileDialog,
    QLineEdit, QMessageBox, QProgressBar, QGroupBox, QFormLayout, QSpinBox, QCheckBox
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import pathlib
import base64
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))
from src.steganografia.image import ImageSteganography

class AdvancedSteganoGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Esteganografía Avanzada - Multiarchivo')
        self.setMinimumSize(800, 600)
        self.tabs = QTabWidget()
        self.tab_hide = QWidget()
        self.tab_extract = QWidget()
        self.tabs.addTab(self.tab_hide, 'Ocultar')
        self.tabs.addTab(self.tab_extract, 'Extraer')
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        self.init_hide_tab()
        self.init_extract_tab()

    def init_hide_tab(self):
        layout = QVBoxLayout()
        # Portadoras
        carrier_group = QGroupBox('Archivos portadora (Imagen, Audio, PDF, etc.)')
        carrier_layout = QVBoxLayout()
        self.carrier_list = QListWidget()
        carrier_btns = QHBoxLayout()
        btn_add_carrier = QPushButton('Agregar portadora')
        btn_add_carrier.clicked.connect(self.add_carrier)
        btn_remove_carrier = QPushButton('Quitar seleccionada')
        btn_remove_carrier.clicked.connect(self.remove_carrier)
        carrier_btns.addWidget(btn_add_carrier)
        carrier_btns.addWidget(btn_remove_carrier)
        carrier_layout.addWidget(self.carrier_list)
        carrier_layout.addLayout(carrier_btns)
        carrier_group.setLayout(carrier_layout)
        layout.addWidget(carrier_group)
        # Archivos secretos
        secret_group = QGroupBox('Archivos a ocultar (cualquier tipo)')
        secret_layout = QVBoxLayout()
        self.secret_list = QListWidget()
        secret_btns = QHBoxLayout()
        btn_add_secret = QPushButton('Agregar archivo secreto')
        btn_add_secret.clicked.connect(self.add_secret)
        btn_remove_secret = QPushButton('Quitar seleccionado')
        btn_remove_secret.clicked.connect(self.remove_secret)
        secret_btns.addWidget(btn_add_secret)
        secret_btns.addWidget(btn_remove_secret)
        secret_layout.addWidget(self.secret_list)
        secret_layout.addLayout(secret_btns)
        secret_group.setLayout(secret_layout)
        layout.addWidget(secret_group)
        # Opciones avanzadas
        options_group = QGroupBox('Opciones avanzadas')
        options_layout = QFormLayout()
        self.password1 = QLineEdit()
        self.password1.setEchoMode(QLineEdit.Password)
        self.password2 = QLineEdit()
        self.password2.setEchoMode(QLineEdit.Password)
        self.password3 = QLineEdit()
        self.password3.setEchoMode(QLineEdit.Password)
        options_layout.addRow('Password A:', self.password1)
        options_layout.addRow('Password B:', self.password2)
        options_layout.addRow('Password C:', self.password3)
        self.bits_spin = QSpinBox()
        self.bits_spin.setRange(1, 8)
        self.bits_spin.setValue(1)
        options_layout.addRow('Bits por canal:', self.bits_spin)
        self.scramble_check = QCheckBox('Scrambling (experimental)')
        options_layout.addRow(self.scramble_check)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        # Comparación de archivos
        compare_group = QGroupBox('Comparación de portadora original vs. modificada')
        compare_layout = QFormLayout()
        self.lbl_orig_size = QLabel('Tamaño original: -')
        self.lbl_mod_size = QLabel('Tamaño modificada: -')
        self.lbl_orig_hash = QLabel('Hash original: -')
        self.lbl_mod_hash = QLabel('Hash modificada: -')
        compare_layout.addRow(self.lbl_orig_size)
        compare_layout.addRow(self.lbl_mod_size)
        compare_layout.addRow(self.lbl_orig_hash)
        compare_layout.addRow(self.lbl_mod_hash)
        compare_group.setLayout(compare_layout)
        layout.addWidget(compare_group)
        # Progreso y acción
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        btn_encode = QPushButton('Ocultar archivos')
        btn_encode.clicked.connect(self.encode_files)
        layout.addWidget(btn_encode)
        self.tab_hide.setLayout(layout)

    def init_extract_tab(self):
        layout = QVBoxLayout()
        carrier_group = QGroupBox('Seleccionar portadora para extraer')
        carrier_layout = QVBoxLayout()
        self.extract_carrier_list = QListWidget()
        carrier_btns = QHBoxLayout()
        btn_add_carrier = QPushButton('Agregar portadora')
        btn_add_carrier.clicked.connect(self.add_extract_carrier)
        btn_remove_carrier = QPushButton('Quitar seleccionada')
        btn_remove_carrier.clicked.connect(self.remove_extract_carrier)
        carrier_btns.addWidget(btn_add_carrier)
        carrier_btns.addWidget(btn_remove_carrier)
        carrier_layout.addWidget(self.extract_carrier_list)
        carrier_layout.addLayout(carrier_btns)
        carrier_group.setLayout(carrier_layout)
        layout.addWidget(carrier_group)
        btn_extract = QPushButton('Extraer archivos ocultos')
        btn_extract.clicked.connect(self.extract_files)
        layout.addWidget(btn_extract)
        self.tab_extract.setLayout(layout)

    def add_carrier(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Seleccionar portadoras', '', 'Todos (*.*)')
        for f in files:
            self.carrier_list.addItem(f)
    def remove_carrier(self):
        for item in self.carrier_list.selectedItems():
            self.carrier_list.takeItem(self.carrier_list.row(item))
    def add_secret(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Seleccionar archivos secretos', '', 'Todos (*.*)')
        for f in files:
            self.secret_list.addItem(f)
    def remove_secret(self):
        for item in self.secret_list.selectedItems():
            self.secret_list.takeItem(self.secret_list.row(item))
    def add_extract_carrier(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Seleccionar portadoras', '', 'Todos (*.*)')
        for f in files:
            self.extract_carrier_list.addItem(f)
    def remove_extract_carrier(self):
        for item in self.extract_carrier_list.selectedItems():
            self.extract_carrier_list.takeItem(self.extract_carrier_list.row(item))
    def encode_files(self):
        if self.carrier_list.count() == 0 or self.secret_list.count() == 0:
            QMessageBox.warning(self, 'Faltan datos', 'Agrega al menos una portadora y un archivo secreto.')
            return
        # Por ahora solo soporta una portadora y un archivo secreto (extensible a varios)
        carrier = self.carrier_list.item(0).text()
        secret = self.secret_list.item(0).text()
        pwd = self.password1.text() or None
        out_path, _ = QFileDialog.getSaveFileName(self, 'Guardar portadora con archivo oculto', '', 'PNG (*.png);;Todos (*.*)')
        if not out_path:
            return
        try:
            import hashlib
            # Mostrar info original
            orig_size = os.path.getsize(carrier)
            with open(carrier, 'rb') as f:
                orig_hash = hashlib.sha256(f.read()).hexdigest()
            self.lbl_orig_size.setText(f'Tamaño original: {orig_size} bytes')
            self.lbl_orig_hash.setText(f'Hash original: {orig_hash}')
            with open(secret, 'rb') as f:
                file_bytes = f.read()
            file_b64 = base64.b64encode(file_bytes).decode('utf-8')
            filename = os.path.basename(secret)
            payload = filename + '||' + file_b64
            ImageSteganography.encode(carrier, out_path, payload, password=pwd, is_binary=False)
            # Mostrar info modificada
            mod_size = os.path.getsize(out_path)
            with open(out_path, 'rb') as f:
                mod_hash = hashlib.sha256(f.read()).hexdigest()
            self.lbl_mod_size.setText(f'Tamaño modificada: {mod_size} bytes')
            self.lbl_mod_hash.setText(f'Hash modificada: {mod_hash}')
            QMessageBox.information(self, 'Éxito', 'Archivo oculto en la portadora.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
    def extract_files(self):
        if self.extract_carrier_list.count() == 0:
            QMessageBox.warning(self, 'Faltan datos', 'Agrega al menos una portadora.')
            return
        carrier = self.extract_carrier_list.item(0).text()
        pwd = self.password1.text() or None
        try:
            # Intentar extraer sin contraseña primero
            try:
                payload = ImageSteganography.decode(carrier, password=None, is_binary=False)
            except Exception as e:
                # Si falla, probablemente requiere contraseña
                if not pwd:
                    QMessageBox.warning(self, 'Contraseña requerida', 'El archivo oculto parece estar protegido. Ingresa la contraseña y vuelve a intentar.')
                    return
                payload = ImageSteganography.decode(carrier, password=pwd, is_binary=False)
            # Si la extracción sin contraseña da un resultado ilegible, pedir contraseña
            if '||' not in payload:
                if not pwd:
                    QMessageBox.warning(self, 'Contraseña requerida', 'El archivo oculto parece estar protegido. Ingresa la contraseña y vuelve a intentar.')
                    return
                payload = ImageSteganography.decode(carrier, password=pwd, is_binary=False)
            header_end = payload.find('||')
            if header_end == -1:
                raise Exception('No se encontró archivo oculto.')
            filename = payload[:header_end]
            file_b64 = payload[header_end+2:]
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
    window = AdvancedSteganoGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
