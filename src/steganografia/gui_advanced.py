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
from src.steganografia.audio import AudioSteganography
from src.steganografia.pdf import PDFSteganography

class AdvancedSteganoGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Esteganografía Avanzada - Multiarchivo')
        self.setMinimumSize(800, 600)
        # Modo oscuro por defecto
        self.apply_dark_mode()
        # Botón de ayuda contextual
        help_btn = QPushButton('Ayuda')
        help_btn.setIcon(QIcon.fromTheme('help-browser'))
        help_btn.setToolTip('Haz clic para ver instrucciones de uso detalladas')
        help_btn.clicked.connect(self.show_help)
        self.tabs = QTabWidget()
        self.tab_hide = QWidget()
        self.tab_extract = QWidget()
        self.tabs.addTab(self.tab_hide, 'Ocultar')
        self.tabs.addTab(self.tab_extract, 'Extraer')
        main_layout = QVBoxLayout()
        main_layout.addWidget(help_btn)
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        self.init_hide_tab()
        self.init_extract_tab()

    def apply_dark_mode(self):
        dark_stylesheet = """
        QWidget { background-color: #232629; color: #f0f0f0; }
        QTabWidget::pane { border: 1px solid #444; }
        QTabBar::tab { background: #2d2f31; color: #f0f0f0; padding: 8px; border: 1px solid #444; border-bottom: none; }
        QTabBar::tab:selected { background: #444; }
        QGroupBox { border: 1px solid #444; margin-top: 10px; }
        QGroupBox:title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }
        QPushButton { background-color: #444; color: #f0f0f0; border: 1px solid #666; padding: 6px; }
        QPushButton:hover { background-color: #555; }
        QListWidget { background: #2d2f31; color: #f0f0f0; border: 1px solid #444; }
        QLineEdit, QSpinBox { background: #232629; color: #f0f0f0; border: 1px solid #444; }
        QProgressBar { background: #2d2f31; color: #f0f0f0; border: 1px solid #444; }
        QLabel { color: #f0f0f0; }
        QCheckBox { color: #f0f0f0; }
        QMessageBox { background-color: #232629; color: #f0f0f0; }
        """
        self.setStyleSheet(dark_stylesheet)

    def show_help(self):
        help_text = (
            "<b>Instrucciones de uso:</b><br><br>"
            "<b>1. Ocultar archivos:</b><br>"
            "- Arrastra o selecciona una <b>portadora</b> (imagen, audio WAV/MP3, PDF) en la sección correspondiente.<br>"
            "- Arrastra o selecciona uno o más <b>archivos secretos</b> a ocultar.<br>"
            "- (Opcional) Ingresa contraseñas para cifrado o ajusta los bits por canal.<br>"
            "- Haz clic en <b>Ocultar archivos</b> para generar la portadora modificada.<br>"
            "- Observa la comparación de tamaño y hash para verificar la operación.<br><br>"
            "<b>2. Extraer archivos:</b><br>"
            "- Selecciona la portadora modificada en la pestaña <b>Extraer</b>.<br>"
            "- (Si corresponde) Ingresa la contraseña usada para ocultar.<br>"
            "- Haz clic en <b>Extraer archivos ocultos</b> y guarda el archivo extraído.<br><br>"
            "<b>Consejos:</b><br>"
            "- Usa imágenes o audios de mayor tamaño para ocultar archivos grandes.<br>"
            "- Si la extracción falla, verifica la contraseña o el tipo de portadora.<br>"
            "- El modo oscuro está activado para facilitar la visualización.<br>"
        )
        QMessageBox.information(self, 'Ayuda - Esteganografía Avanzada', help_text)

    def init_hide_tab(self):
        layout = QVBoxLayout()
        # Portadoras
        carrier_group = QGroupBox('Archivos portadora (Imagen, Audio, PDF, etc.)')
        carrier_layout = QVBoxLayout()
        self.carrier_list = QListWidget()
        self.carrier_list.setToolTip('Arrastra aquí archivos portadora (imagen, audio, PDF) o usa el botón para agregarlos.')
        self.carrier_list.setSelectionMode(self.carrier_list.SingleSelection)
        self.carrier_list.setAcceptDrops(True)
        self.carrier_list.dragEnterEvent = lambda e: e.accept() if e.mimeData().hasUrls() else e.ignore()
        self.carrier_list.dropEvent = self.drop_carrier_event
        # Vista previa de portadora
        self.lbl_preview = QLabel('Vista previa de portadora')
        self.lbl_preview.setAlignment(Qt.AlignCenter)
        carrier_layout.addWidget(self.lbl_preview)
        carrier_btns = QHBoxLayout()
        btn_add_carrier = QPushButton('Agregar portadora')
        btn_add_carrier.setToolTip('Selecciona un archivo portadora (imagen, audio, PDF)')
        btn_add_carrier.clicked.connect(self.add_carrier)
        btn_remove_carrier = QPushButton('Quitar seleccionada')
        btn_remove_carrier.setToolTip('Quita la portadora seleccionada de la lista')
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
        self.secret_list.setToolTip('Arrastra aquí archivos secretos o usa el botón para agregarlos.')
        self.secret_list.setAcceptDrops(True)
        self.secret_list.dragEnterEvent = lambda e: e.accept() if e.mimeData().hasUrls() else e.ignore()
        self.secret_list.dropEvent = self.drop_secret_event
        secret_btns = QHBoxLayout()
        btn_add_secret = QPushButton('Agregar archivo secreto')
        btn_add_secret.setToolTip('Selecciona un archivo a ocultar')
        btn_add_secret.clicked.connect(self.add_secret)
        btn_remove_secret = QPushButton('Quitar seleccionado')
        btn_remove_secret.setToolTip('Quita el archivo secreto seleccionado de la lista')
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

    def drop_carrier_event(self, event):
        for url in event.mimeData().urls():
            f = url.toLocalFile()
            self.carrier_list.addItem(f)
            self.update_preview(f)
        event.accept()

    def update_preview(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
            pixmap = QPixmap(file_path)
            self.lbl_preview.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio))
        elif ext in ['.wav', '.mp3']:
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText('Audio seleccionado: ' + os.path.basename(file_path))
        elif ext == '.pdf':
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText('PDF seleccionado: ' + os.path.basename(file_path))
        else:
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText('Vista previa no disponible')

    def drop_secret_event(self, event):
        for url in event.mimeData().urls():
            f = url.toLocalFile()
            self.secret_list.addItem(f)
        event.accept()

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
        if files:
            self.update_preview(files[0])
    def remove_carrier(self):
        for item in self.carrier_list.selectedItems():
            self.carrier_list.takeItem(self.carrier_list.row(item))
        # Limpiar vista previa si no hay portadoras
        if self.carrier_list.count() == 0:
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText('Vista previa de portadora')
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
        carrier = self.carrier_list.item(0).text()
        secret = self.secret_list.item(0).text()
        pwd = self.password1.text() or None
        # Detectar tipo de portadora
        ext = os.path.splitext(carrier)[1].lower()
        if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
            file_filter = 'PNG (*.png);;Todos (*.*)'
        elif ext in ['.wav']:
            file_filter = 'WAV (*.wav);;Todos (*.*)'
        elif ext in ['.mp3']:
            file_filter = 'MP3 (*.mp3);;Todos (*.*)'
        elif ext == '.pdf':
            file_filter = 'PDF (*.pdf);;Todos (*.*)'
        else:
            file_filter = 'Todos (*.*)'
        out_path, _ = QFileDialog.getSaveFileName(self, 'Guardar portadora con archivo oculto', '', file_filter)
        if not out_path:
            return
        try:
            import hashlib
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
            # Lógica según tipo de portadora
            if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                ImageSteganography.encode(carrier, out_path, payload, password=pwd, is_binary=False)
            elif ext == '.wav':
                AudioSteganography.encode_wav(carrier, out_path, payload, password=pwd)
            elif ext == '.mp3':
                AudioSteganography.encode_mp3(carrier, out_path, payload, password=pwd)
            elif ext == '.pdf':
                PDFSteganography.encode(carrier, out_path, payload, password=pwd)
            else:
                raise Exception('Tipo de portadora no soportado aún.')
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
        ext = os.path.splitext(carrier)[1].lower()
        try:
            # Lógica según tipo de portadora
            if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                decode_func = lambda p: ImageSteganography.decode(p, password=pwd, is_binary=False)
            elif ext == '.wav':
                decode_func = lambda p: AudioSteganography.decode_wav(p, password=pwd)
            elif ext == '.mp3':
                decode_func = lambda p: AudioSteganography.decode_mp3(p, password=pwd)
            elif ext == '.pdf':
                decode_func = lambda p: PDFSteganography.decode(p, password=pwd)
            else:
                raise Exception('Tipo de portadora no soportado aún.')
            # Intentar extraer sin contraseña primero si es imagen
            payload = None
            if ext in ['.png', '.jpg', '.jpeg', '.bmp'] and not pwd:
                try:
                    payload = ImageSteganography.decode(carrier, password=None, is_binary=False)
                except Exception:
                    pass
            if not payload:
                payload = decode_func(carrier)
            if '||' not in payload:
                if not pwd:
                    QMessageBox.warning(self, 'Contraseña requerida', 'El archivo oculto parece estar protegido. Ingresa la contraseña y vuelve a intentar.')
                    return
                payload = decode_func(carrier)
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
