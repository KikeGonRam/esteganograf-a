import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QFileDialog,
    QLineEdit, QMessageBox, QProgressBar, QGroupBox, QFormLayout, QSpinBox, QCheckBox, QScrollArea
)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor
from PyQt5.QtCore import Qt, QSize
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
        self.setMinimumSize(1100, 750)
        self.apply_professional_theme()
        self.init_ui()

    def apply_professional_theme(self):
        """Aplica un tema profesional moderno"""
        professional_stylesheet = """
        QWidget { 
            background-color: #0d1117; 
            color: #e0e0e0; 
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 10pt;
        }
        QTabWidget::pane { 
            border: 1px solid #30363d; 
            background-color: #0d1117;
        }
        QTabBar::tab { 
            background: #161b22; 
            color: #8b949e; 
            padding: 12px 24px; 
            border: 1px solid #30363d;
            margin-right: 0px;
            font-weight: 500;
        }
        QTabBar::tab:selected { 
            background: #1f6feb; 
            color: #ffffff;
            border: 1px solid #1f6feb;
        }
        QTabBar::tab:hover { 
            background: #262d34;
        }
        QGroupBox { 
            border: 1px solid #30363d; 
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: 500;
            color: #58a6ff;
        }
        QGroupBox:title { 
            subcontrol-origin: margin; 
            left: 12px; 
            padding: 0 4px 0 4px;
        }
        QPushButton { 
            background-color: #1f6feb;
            color: #ffffff; 
            border: 1px solid #1f6feb; 
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 500;
        }
        QPushButton:hover { 
            background-color: #388bfd;
            border: 1px solid #388bfd;
        }
        QPushButton:pressed { 
            background-color: #1a4fab;
        }
        QPushButton:disabled {
            background-color: #30363d;
            color: #6e7681;
            border: 1px solid #30363d;
        }
        QListWidget { 
            background: #0d1117; 
            color: #c9d1d9; 
            border: 1px solid #30363d; 
            border-radius: 4px;
            padding: 4px;
        }
        QListWidget::item { 
            padding: 6px 4px; 
            border-radius: 3px;
        }
        QListWidget::item:selected { 
            background: #1f6feb; 
            color: #ffffff;
        }
        QListWidget::item:hover { 
            background: #161b22;
        }
        QLineEdit { 
            background: #0d1117; 
            color: #c9d1d9; 
            border: 1px solid #30363d; 
            border-radius: 4px;
            padding: 6px 8px;
            selection-background-color: #1f6feb;
        }
        QLineEdit:focus { 
            border: 1px solid #58a6ff;
            background: #0d1117;
        }
        QSpinBox { 
            background: #0d1117; 
            color: #c9d1d9; 
            border: 1px solid #30363d; 
            border-radius: 4px;
            padding: 4px;
        }
        QSpinBox:focus { 
            border: 1px solid #58a6ff;
        }
        QSpinBox::up-button, QSpinBox::down-button {
            background: #161b22;
            border: 1px solid #30363d;
        }
        QProgressBar { 
            background: #161b22; 
            color: #c9d1d9; 
            border: 1px solid #30363d; 
            border-radius: 4px;
            text-align: center;
            height: 6px;
        }
        QProgressBar::chunk { 
            background: #1f6feb;
            border-radius: 3px;
        }
        QCheckBox { 
            color: #c9d1d9;
            spacing: 6px;
        }
        QCheckBox::indicator { 
            width: 16px; 
            height: 16px;
        }
        QCheckBox::indicator:unchecked { 
            background: #0d1117; 
            border: 1px solid #30363d;
            border-radius: 3px;
        }
        QCheckBox::indicator:checked { 
            background: #1f6feb; 
            border: 1px solid #1f6feb;
            border-radius: 3px;
        }
        QLabel { 
            color: #c9d1d9;
        }
        QScrollArea {
            background: #0d1117;
            border: none;
        }
        """
        self.setStyleSheet(professional_stylesheet)

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel('Esteganografía Avanzada')
        title_font = QFont('Segoe UI', 12, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #58a6ff;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        help_btn = QPushButton('Ayuda')
        help_btn.setMaximumWidth(100)
        help_btn.clicked.connect(self.show_help)
        header_layout.addWidget(help_btn)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tab_hide = QWidget()
        self.tab_extract = QWidget()
        self.tab_compare = QWidget()
        self.tabs.addTab(self.tab_hide, 'Ocultar')
        self.tabs.addTab(self.tab_extract, 'Extraer')
        self.tabs.addTab(self.tab_compare, 'Análisis')
        main_layout.addWidget(self.tabs)
        
        self.setLayout(main_layout)
        self.init_hide_tab()
        self.init_extract_tab()
        self.init_compare_tab()

    def show_help(self):
        help_text = (
            "<b>Instrucciones de Uso</b><br><br>"
            "<b>Ocultar archivos:</b><br>"
            "1. Selecciona una portadora (imagen, audio WAV/MP3, PDF)<br>"
            "2. Agrega uno o más archivos secretos a ocultar<br>"
            "3. (Opcional) Establece contraseñas para cifrado<br>"
            "4. Haz clic en 'Ocultar Archivos'<br>"
            "5. Verifica el análisis para confirmar la operación<br><br>"
            "<b>Extraer archivos:</b><br>"
            "1. Selecciona la portadora modificada<br>"
            "2. Ingresa la contraseña (si la hay)<br>"
            "3. Haz clic en 'Extraer Archivos Ocultos'<br>"
            "4. Guarda el archivo extraído<br><br>"
            "<b>Análisis:</b><br>"
            "Visualiza el historial de operaciones y comparación de archivos."
        )
        msg = QMessageBox(self)
        msg.setWindowTitle('Ayuda - Esteganografía Avanzada')
        msg.setText(help_text)
        msg.exec_()

    def init_hide_tab(self):
        layout = QVBoxLayout()
        
        # Portadoras
        carrier_group = QGroupBox('Archivo Portadora')
        carrier_layout = QVBoxLayout()
        
        self.lbl_preview = QLabel('Vista previa de portadora')
        self.lbl_preview.setAlignment(Qt.AlignCenter)
        self.lbl_preview.setStyleSheet("padding: 20px; border: 1px dashed #30363d; border-radius: 4px; min-height: 100px; background: #161b22;")
        self.lbl_preview.setMinimumHeight(120)
        carrier_layout.addWidget(self.lbl_preview)
        
        self.carrier_list = QListWidget()
        self.carrier_list.setMaximumHeight(60)
        self.carrier_list.setAcceptDrops(True)
        self.carrier_list.dragEnterEvent = lambda e: e.accept() if e.mimeData().hasUrls() else e.ignore()
        self.carrier_list.dropEvent = self.drop_carrier_event
        carrier_layout.addWidget(self.carrier_list)
        
        carrier_btns = QHBoxLayout()
        btn_add_carrier = QPushButton('Agregar Portadora')
        btn_add_carrier.clicked.connect(self.add_carrier)
        btn_remove_carrier = QPushButton('Quitar')
        btn_remove_carrier.clicked.connect(self.remove_carrier)
        carrier_btns.addWidget(btn_add_carrier)
        carrier_btns.addWidget(btn_remove_carrier)
        carrier_layout.addLayout(carrier_btns)
        carrier_group.setLayout(carrier_layout)
        layout.addWidget(carrier_group)

        # Archivos secretos
        secret_group = QGroupBox('Archivos a Ocultar')
        secret_layout = QVBoxLayout()
        self.secret_list = QListWidget()
        self.secret_list.setAcceptDrops(True)
        self.secret_list.dragEnterEvent = lambda e: e.accept() if e.mimeData().hasUrls() else e.ignore()
        self.secret_list.dropEvent = self.drop_secret_event
        secret_layout.addWidget(self.secret_list)
        
        secret_btns = QHBoxLayout()
        btn_add_secret = QPushButton('Agregar Archivo')
        btn_add_secret.clicked.connect(self.add_secret)
        btn_remove_secret = QPushButton('Quitar')
        btn_remove_secret.clicked.connect(self.remove_secret)
        secret_btns.addWidget(btn_add_secret)
        secret_btns.addWidget(btn_remove_secret)
        secret_layout.addLayout(secret_btns)
        secret_group.setLayout(secret_layout)
        layout.addWidget(secret_group)

        # Opciones avanzadas
        options_group = QGroupBox('Opciones Avanzadas')
        options_layout = QFormLayout()
        
        self.password1 = QLineEdit()
        self.password1.setPlaceholderText('Contraseña principal')
        self.password1.setEchoMode(QLineEdit.Password)
        
        self.password2 = QLineEdit()
        self.password2.setPlaceholderText('Contraseña alternativa')
        self.password2.setEchoMode(QLineEdit.Password)
        
        self.password3 = QLineEdit()
        self.password3.setPlaceholderText('Contraseña adicional')
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

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        btn_encode = QPushButton('Ocultar Archivos')
        btn_encode.setMinimumHeight(40)
        btn_encode.setFont(QFont('Segoe UI', 10, QFont.Bold))
        btn_encode.clicked.connect(self.encode_files)
        layout.addWidget(btn_encode)
        
        layout.addStretch()
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
            scaled = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lbl_preview.setPixmap(scaled)
        elif ext in ['.wav', '.mp3']:
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText(f'Audio: {os.path.basename(file_path)}')
        elif ext == '.pdf':
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText(f'PDF: {os.path.basename(file_path)}')
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
        carrier_group = QGroupBox('Seleccionar Portadora')
        carrier_layout = QVBoxLayout()
        self.extract_carrier_list = QListWidget()
        carrier_layout.addWidget(self.extract_carrier_list)
        
        carrier_btns = QHBoxLayout()
        btn_add_carrier = QPushButton('Agregar')
        btn_add_carrier.clicked.connect(self.add_extract_carrier)
        btn_remove_carrier = QPushButton('Quitar')
        btn_remove_carrier.clicked.connect(self.remove_extract_carrier)
        carrier_btns.addWidget(btn_add_carrier)
        carrier_btns.addWidget(btn_remove_carrier)
        carrier_layout.addLayout(carrier_btns)
        carrier_group.setLayout(carrier_layout)
        layout.addWidget(carrier_group)
        
        pwd_group = QGroupBox('Contraseña')
        pwd_layout = QFormLayout()
        self.extract_password = QLineEdit()
        self.extract_password.setPlaceholderText('Ingresa contraseña si el archivo está cifrado')
        self.extract_password.setEchoMode(QLineEdit.Password)
        pwd_layout.addRow(self.extract_password)
        pwd_group.setLayout(pwd_layout)
        layout.addWidget(pwd_group)
        
        layout.addStretch()
        
        btn_extract = QPushButton('Extraer Archivos Ocultos')
        btn_extract.setMinimumHeight(40)
        btn_extract.setFont(QFont('Segoe UI', 10, QFont.Bold))
        btn_extract.clicked.connect(self.extract_files)
        layout.addWidget(btn_extract)
        
        self.tab_extract.setLayout(layout)

    def init_compare_tab(self):
        layout = QVBoxLayout()
        info_label = QLabel('Información de Análisis')
        info_font = QFont('Segoe UI', 11, QFont.Bold)
        info_label.setFont(info_font)
        info_label.setStyleSheet("color: #58a6ff;")
        layout.addWidget(info_label)

        # Selección y previsualización de archivos
        select_group = QGroupBox('Selecciona archivos para comparar')
        select_layout = QHBoxLayout()
        # Original
        orig_layout = QVBoxLayout()
        self.btn_select_orig = QPushButton('Seleccionar original')
        self.btn_select_orig.clicked.connect(self.select_orig_file)
        self.lbl_orig_preview = QLabel('Vista previa original')
        self.lbl_orig_preview.setAlignment(Qt.AlignCenter)
        self.lbl_orig_preview.setMinimumHeight(100)
        orig_layout.addWidget(self.btn_select_orig)
        orig_layout.addWidget(self.lbl_orig_preview)
        # Modificado
        mod_layout = QVBoxLayout()
        self.btn_select_mod = QPushButton('Seleccionar modificado')
        self.btn_select_mod.clicked.connect(self.select_mod_file)
        self.lbl_mod_preview = QLabel('Vista previa modificada')
        self.lbl_mod_preview.setAlignment(Qt.AlignCenter)
        self.lbl_mod_preview.setMinimumHeight(100)
        mod_layout.addWidget(self.btn_select_mod)
        mod_layout.addWidget(self.lbl_mod_preview)
        select_layout.addLayout(orig_layout)
        select_layout.addLayout(mod_layout)
        select_group.setLayout(select_layout)
        layout.addWidget(select_group)

        # Información de análisis
        compare_group = QGroupBox('Portadora Original')
        compare_layout = QFormLayout()
        self.lbl_orig_size = QLabel('Tamaño: -')
        self.lbl_orig_hash = QLabel('Hash SHA256: -')
        self.lbl_orig_size.setStyleSheet("padding: 6px; background: #161b22; border-radius: 3px;")
        self.lbl_orig_hash.setStyleSheet("padding: 6px; background: #161b22; border-radius: 3px;")
        compare_layout.addRow(self.lbl_orig_size)
        compare_layout.addRow(self.lbl_orig_hash)
        compare_group.setLayout(compare_layout)
        layout.addWidget(compare_group)

        compare_group2 = QGroupBox('Portadora Modificada')
        compare_layout2 = QFormLayout()
        self.lbl_mod_size = QLabel('Tamaño: -')
        self.lbl_mod_hash = QLabel('Hash SHA256: -')
        self.lbl_mod_size.setStyleSheet("padding: 6px; background: #161b22; border-radius: 3px;")
        self.lbl_mod_hash.setStyleSheet("padding: 6px; background: #161b22; border-radius: 3px;")
        compare_layout2.addRow(self.lbl_mod_size)
        compare_layout2.addRow(self.lbl_mod_hash)
        compare_group2.setLayout(compare_layout2)
        layout.addWidget(compare_group2)

        diff_group = QGroupBox('Diferencia de Tamaño')
        diff_layout = QFormLayout()
        self.lbl_diff_size = QLabel('Diferencia: -')
        self.lbl_diff_size.setStyleSheet("padding: 6px; background: #161b22; border-radius: 3px;")
        diff_layout.addRow(self.lbl_diff_size)
        diff_group.setLayout(diff_layout)
        layout.addWidget(diff_group)

        layout.addStretch()

        btn_clear = QPushButton('Limpiar Análisis')
        btn_clear.clicked.connect(self.clear_analysis)
        layout.addWidget(btn_clear)

        self.tab_compare.setLayout(layout)

    def select_orig_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Seleccionar archivo original', '', 'Todos (*.*)')
        if file:
            self.show_preview(file, self.lbl_orig_preview)
            self.update_analysis_info(file, is_original=True)
            self.orig_file = file
            self.update_diff()

    def select_mod_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Seleccionar archivo modificado', '', 'Todos (*.*)')
        if file:
            self.show_preview(file, self.lbl_mod_preview)
            self.update_analysis_info(file, is_original=False)
            self.mod_file = file
            self.update_diff()

    def show_preview(self, file_path, label):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
            pixmap = QPixmap(file_path)
            label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio))
            label.setText('')
        elif ext in ['.wav', '.mp3']:
            label.setPixmap(QPixmap())
            label.setText('Audio: ' + os.path.basename(file_path))
        elif ext == '.pdf':
            label.setPixmap(QPixmap())
            label.setText('PDF: ' + os.path.basename(file_path))
        else:
            label.setPixmap(QPixmap())
            label.setText('Vista previa no disponible')

    def update_analysis_info(self, file_path, is_original):
        import hashlib
        try:
            size = os.path.getsize(file_path)
            with open(file_path, 'rb') as f:
                hashv = hashlib.sha256(f.read()).hexdigest()
        except Exception:
            size = '-'
            hashv = '-'
        if is_original:
            self.lbl_orig_size.setText(f'Tamaño: {size} bytes')
            self.lbl_orig_hash.setText(f'Hash SHA256: {hashv}')
        else:
            self.lbl_mod_size.setText(f'Tamaño: {size} bytes')
            self.lbl_mod_hash.setText(f'Hash SHA256: {hashv}')

    def update_diff(self):
        try:
            orig = getattr(self, 'orig_file', None)
            mod = getattr(self, 'mod_file', None)
            if orig and mod:
                size1 = os.path.getsize(orig)
                size2 = os.path.getsize(mod)
                diff = size2 - size1
                self.lbl_diff_size.setText(f'Diferencia: {diff} bytes')
            else:
                self.lbl_diff_size.setText('Diferencia: -')
        except Exception:
            self.lbl_diff_size.setText('Diferencia: -')

    def clear_analysis(self):
        self.lbl_orig_size.setText('Tamaño: -')
        self.lbl_orig_hash.setText('Hash SHA256: -')
        self.lbl_mod_size.setText('Tamaño: -')
        self.lbl_mod_hash.setText('Hash SHA256: -')
        self.lbl_diff_size.setText('Diferencia: -')

    def add_carrier(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Seleccionar Portadoras', '', 
            'Imágenes (*.png *.jpg *.jpeg *.bmp);;Audio (*.wav *.mp3);;PDF (*.pdf);;Todos (*.*)')
        for f in files:
            self.carrier_list.addItem(f)
        if files:
            self.update_preview(files[0])

    def remove_carrier(self):
        for item in self.carrier_list.selectedItems():
            self.carrier_list.takeItem(self.carrier_list.row(item))
        if self.carrier_list.count() == 0:
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText('Vista previa de portadora')

    def add_secret(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Seleccionar Archivos Secretos', '', 'Todos (*.*)')
        for f in files:
            self.secret_list.addItem(f)

    def remove_secret(self):
        for item in self.secret_list.selectedItems():
            self.secret_list.takeItem(self.secret_list.row(item))

    def add_extract_carrier(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Seleccionar Portadora', '', 
            'Imágenes (*.png *.jpg *.jpeg *.bmp);;Audio (*.wav *.mp3);;PDF (*.pdf);;Todos (*.*)')
        for f in files:
            self.extract_carrier_list.addItem(f)

    def remove_extract_carrier(self):
        for item in self.extract_carrier_list.selectedItems():
            self.extract_carrier_list.takeItem(self.extract_carrier_list.row(item))

    def encode_files(self):
        if self.carrier_list.count() == 0 or self.secret_list.count() == 0:
            QMessageBox.warning(self, 'Datos Faltantes', 'Agrega al menos una portadora y un archivo secreto.')
            return
        carrier = self.carrier_list.item(0).text()
        secret = self.secret_list.item(0).text()
        pwd = self.password1.text() or None
        ext = os.path.splitext(carrier)[1].lower()
        
        if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
            file_filter = 'PNG (*.png);;JPG (*.jpg);;Todos (*.*)'
        elif ext == '.wav':
            file_filter = 'WAV (*.wav);;Todos (*.*)'
        elif ext == '.mp3':
            file_filter = 'MP3 (*.mp3);;Todos (*.*)'
        elif ext == '.pdf':
            file_filter = 'PDF (*.pdf);;Todos (*.*)'
        else:
            file_filter = 'Todos (*.*)'
        
        out_path, _ = QFileDialog.getSaveFileName(self, 'Guardar Portadora Modificada', '', file_filter)
        if not out_path:
            return
        
        try:
            self.progress.setVisible(True)
            self.progress.setValue(30)
            
            import hashlib
            orig_size = os.path.getsize(carrier)
            with open(carrier, 'rb') as f:
                orig_hash = hashlib.sha256(f.read()).hexdigest()
            self.lbl_orig_size.setText(f'Tamaño: {orig_size} bytes')
            self.lbl_orig_hash.setText(f'Hash SHA256: {orig_hash}')
            
            with open(secret, 'rb') as f:
                file_bytes = f.read()
            file_b64 = base64.b64encode(file_bytes).decode('utf-8')
            filename = os.path.basename(secret)
            payload = filename + '||' + file_b64
            
            self.progress.setValue(60)
            
            if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                ImageSteganography.encode(carrier, out_path, payload, password=pwd, is_binary=False)
            elif ext == '.wav':
                AudioSteganography.encode_wav(carrier, out_path, payload, password=pwd)
            elif ext == '.mp3':
                AudioSteganography.encode_mp3(carrier, out_path, payload, password=pwd)
            elif ext == '.pdf':
                PDFSteganography.encode(carrier, out_path, payload, password=pwd)
            
            self.progress.setValue(90)
            
            mod_size = os.path.getsize(out_path)
            with open(out_path, 'rb') as f:
                mod_hash = hashlib.sha256(f.read()).hexdigest()
            self.lbl_mod_size.setText(f'Tamaño: {mod_size} bytes')
            self.lbl_mod_hash.setText(f'Hash SHA256: {mod_hash}')
            
            diff_size = mod_size - orig_size
            self.lbl_diff_size.setText(f'Diferencia: {diff_size} bytes')
            
            self.progress.setValue(100)
            self.tabs.setCurrentIndex(2)
            QMessageBox.information(self, 'Éxito', f'Archivo oculto exitosamente.\n\nGuardado: {os.path.basename(out_path)}')
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al ocultar: {str(e)}')
        finally:
            self.progress.setVisible(False)

    def extract_files(self):
        if self.extract_carrier_list.count() == 0:
            QMessageBox.warning(self, 'Datos Faltantes', 'Selecciona una portadora para extraer.')
            return
        
        carrier = self.extract_carrier_list.item(0).text()
        pwd = self.extract_password.text() or None
        ext = os.path.splitext(carrier)[1].lower()
        
        try:
            if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                payload = ImageSteganography.decode(carrier, password=pwd, is_binary=False)
            elif ext == '.wav':
                payload = AudioSteganography.decode_wav(carrier, password=pwd)
            elif ext == '.mp3':
                payload = AudioSteganography.decode_mp3(carrier, password=pwd)
            elif ext == '.pdf':
                payload = PDFSteganography.decode(carrier, password=pwd)
            else:
                raise Exception('Tipo de portadora no soportado.')
            
            if '||' not in payload:
                if not pwd:
                    QMessageBox.warning(self, 'Contraseña Requerida', 'El archivo parece estar cifrado. Ingresa la contraseña.')
                    return
            
            header_end = payload.find('||')
            if header_end == -1:
                raise Exception('No se encontró archivo oculto válido.')
            
            filename = payload[:header_end]
            file_b64 = payload[header_end+2:]
            file_bytes = base64.b64decode(file_b64)
            
            save_path, _ = QFileDialog.getSaveFileName(self, 'Guardar Archivo Extraído', filename)
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(file_bytes)
                QMessageBox.information(self, 'Éxito', f'Archivo extraído: {os.path.basename(save_path)}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al extraer: {str(e)}')

def main():
    app = QApplication(sys.argv)
    window = AdvancedSteganoGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()