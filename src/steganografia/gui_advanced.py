import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QFileDialog,
    QLineEdit, QMessageBox, QProgressBar, QGroupBox, QFormLayout, QSpinBox, QCheckBox, QScrollArea, QComboBox
)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor
from PyQt5.QtCore import Qt, QSize, QTranslator, QLocale
import pathlib
import base64
from zip import ZipSteganography
from docx_steg import DocxSteganography
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from utils.crypto import encrypt_message, decrypt_message
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))
from src.steganografia.image import ImageSteganography
from src.steganografia.audio import AudioSteganography
from src.steganografia.pdf import PDFSteganography

class AdvancedSteganoGUI(QWidget):
    def show_help(self):
        QMessageBox.information(
            self,
            'Ayuda',
            'Esteganografía avanzada:\n'
            '- Usa las pestañas para ocultar, extraer, analizar y ver historial de operaciones.\n'
            '- Arrastra y suelta archivos o usa los botones para agregarlos.\n'
            '- El historial registra cada acción realizada.\n'
            '- Para más detalles, consulta la documentación o README.'
        )
    def __init__(self):
        super().__init__()
        self.translator = QTranslator()
        self.setWindowTitle('Esteganografía Avanzada - Multiarchivo')
        self.setMinimumSize(1100, 750)
        self.apply_professional_theme()
        self.history = []  # Lista de historial de operaciones
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
        # --- Multilenguaje ---
        self.language_combo = QComboBox()
        self.language_combo.addItems(['Español', 'English'])
        self.language_combo.currentIndexChanged.connect(self.change_language)
        # --- Temas ---
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Oscuro', 'Claro'])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel('Tema:'))
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        # --- Layout superior ---
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.language_combo)
        top_layout.addLayout(theme_layout)
        main_layout.addLayout(top_layout)
        # Header
        header_layout = QHBoxLayout()
        self.title_label = QLabel('Esteganografía Avanzada')
        title_font = QFont('Segoe UI', 12, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #58a6ff;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        self.help_btn = QPushButton('Ayuda')
        self.help_btn.setMaximumWidth(100)
        self.help_btn.clicked.connect(self.show_help)
        header_layout.addWidget(self.help_btn)
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        # Tabs
        self.tabs = QTabWidget()
        self.tab_hide = QWidget()
        self.tab_extract = QWidget()
        self.tab_compare = QWidget()
        self.tab_history = QWidget()
        self.tabs.addTab(self.tab_hide, 'Ocultar')
        self.tabs.addTab(self.tab_extract, 'Extraer')
        self.tabs.addTab(self.tab_compare, 'Análisis')
        self.tabs.addTab(self.tab_history, 'Historial')
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        # Inicializar contenido de cada pestaña
        self.init_hide_tab()
        self.init_extract_tab()
        self.init_compare_tab()
        self.init_history_tab()

    def change_theme(self, idx):
        theme = self.theme_combo.currentText()
        if theme == 'Claro':
            self.apply_light_theme()
        else:
            self.apply_professional_theme()

    def apply_light_theme(self):
        light_stylesheet = """
        QWidget {
            background-color: #f5f5f5;
            color: #222222;
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 10pt;
        }
        QTabWidget::pane {
            border: 1px solid #cccccc;
            background-color: #f5f5f5;
        }
        QTabBar::tab {
            background: #e0e0e0;
            color: #222222;
            padding: 12px 24px;
            border: 1px solid #cccccc;
            margin-right: 0px;
            font-weight: 500;
        }
        QTabBar::tab:selected {
            background: #1976d2;
            color: #ffffff;
            border: 1px solid #1976d2;
        }
        QTabBar::tab:hover {
            background: #eeeeee;
        }
        QGroupBox {
            border: 1px solid #cccccc;
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: 500;
            color: #1976d2;
        }
        QGroupBox:title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 4px 0 4px;
        }
        QPushButton {
            background-color: #1976d2;
            color: #ffffff;
            border: 1px solid #1976d2;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #2196f3;
            border: 1px solid #2196f3;
        }
        QPushButton:pressed {
            background-color: #1565c0;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #888888;
            border: 1px solid #cccccc;
        }
        QListWidget {
            background: #f5f5f5;
            color: #222222;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 4px;
        }
        QListWidget::item {
            padding: 6px 4px;
            border-radius: 3px;
        }
        QListWidget::item:selected {
            background: #1976d2;
            color: #ffffff;
        }
        QListWidget::item:hover {
            background: #e0e0e0;
        }
        QLineEdit {
            background: #ffffff;
            color: #222222;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 6px 8px;
            selection-background-color: #1976d2;
        }
        QLineEdit:focus {
            border: 1px solid #1976d2;
            background: #ffffff;
        }
        QSpinBox {
            background: #ffffff;
            color: #222222;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 4px;
        }
        QSpinBox:focus {
            border: 1px solid #1976d2;
        }
        QSpinBox::up-button, QSpinBox::down-button {
            background: #e0e0e0;
            border: 1px solid #cccccc;
        }
        QProgressBar {
            background: #e0e0e0;
            color: #222222;
            border: 1px solid #cccccc;
            border-radius: 4px;
            text-align: center;
            height: 6px;
        }
        QProgressBar::chunk {
            background: #1976d2;
            border-radius: 3px;
        }
        QCheckBox {
            color: #222222;
            spacing: 6px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        QCheckBox::indicator:unchecked {
            background: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 3px;
        }
        QCheckBox::indicator:checked {
            background: #1976d2;
            border: 1px solid #1976d2;
            border-radius: 3px;
        }
        QLabel {
            color: #222222;
        }
        QScrollArea {
            background: #f5f5f5;
            border: none;
        }
        """
        self.setStyleSheet(light_stylesheet)

    def change_language(self, idx):
        lang = self.language_combo.currentText()
        if lang == 'English':
            if self.translator.load('en.qm'):
                QApplication.instance().installTranslator(self.translator)
        else:
            QApplication.instance().removeTranslator(self.translator)
        self.retranslateUi()

    def retranslateUi(self):
        # Aquí se actualizarían los textos de los widgets si se usan tr() o se recargan manualmente
        self.setWindowTitle(self.tr('Esteganografía Avanzada - Multiarchivo'))
        self.title_label.setText(self.tr('Esteganografía Avanzada'))
        self.help_btn.setText(self.tr('Ayuda'))
        self.tabs.setTabText(0, self.tr('Ocultar'))
        self.tabs.setTabText(1, self.tr('Extraer'))
        self.tabs.setTabText(2, self.tr('Análisis'))
        self.tabs.setTabText(3, self.tr('Historial'))
        # ...actualizar más textos según sea necesario...
    def init_history_tab(self):
        layout = QVBoxLayout()
        self.history_list = QListWidget()
        self.history_list.setSelectionMode(QListWidget.NoSelection)
        layout.addWidget(self.history_list)
        btns = QHBoxLayout()
        btn_clear = QPushButton('Limpiar Historial')
        btn_clear.clicked.connect(self.clear_history)
        btns.addStretch()
        btns.addWidget(btn_clear)
        layout.addLayout(btns)
        self.tab_history.setLayout(layout)

    def add_history_entry(self, action, files, result):
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = {
            'hora': timestamp,
            'accion': action,
            'archivos': files,
            'resultado': result
        }
        self.history.append(entry)
        # Mostrar en la lista
        files_str = ', '.join(files) if isinstance(files, list) else str(files)
        text = f"[{timestamp}] {action} | Archivos: {files_str} | Resultado: {result}"
        self.history_list.addItem(text)

    def clear_history(self):
        self.history.clear()
        self.history_list.clear()

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
        self.secret_list.setDragEnabled(True)
        self.secret_list.dragEnterEvent = lambda e: e.accept() if e.mimeData().hasUrls() else e.ignore()
        self.secret_list.dropEvent = self.drop_secret_event
        # (Eliminada definición anidada y duplicada de init_compare_tab)
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

        from PyQt5.QtWidgets import QComboBox
        self.cipher_combo = QComboBox()
        self.cipher_combo.addItems(['Fernet', 'AES'])
        options_layout.addRow('Password A:', self.password1)
        options_layout.addRow('Password B:', self.password2)
        options_layout.addRow('Password C:', self.password3)
        options_layout.addRow('Algoritmo de cifrado:', self.cipher_combo)
        
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
            self.lbl_preview.setText('')
        elif ext in ['.wav', '.mp3']:
            try:
                from pydub.utils import mediainfo
                info = mediainfo(file_path)
                duration = float(info.get('duration', 0))
                duration_str = f"{duration:.1f} seg" if duration else "-"
            except Exception:
                duration_str = "-"
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText(f'Audio: {os.path.basename(file_path)}\nDuración: {duration_str}')
        elif ext == '.pdf':
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(file_path)
                if reader.pages:
                    page = reader.pages[0]
                    text = page.extract_text()[:100] if page.extract_text() else "(Sin texto extraíble)"
                else:
                    text = "(PDF vacío)"
            except Exception:
                text = "(No se pudo leer PDF)"
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText(f'PDF: {os.path.basename(file_path)}\nExtracto: {text}')
        elif ext in ['.mp4', '.avi', '.mov']:
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText(f'Video: {os.path.basename(file_path)}')
        elif ext == '.docx':
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText(f'Word DOCX: {os.path.basename(file_path)}')
        elif ext == '.zip':
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText(f'ZIP: {os.path.basename(file_path)}')
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
            # Registrar en historial si ambos archivos están seleccionados
            if hasattr(self, 'mod_file') and self.mod_file:
                self.add_history_entry(
                    'Análisis',
                    [file, self.mod_file],
                    'Comparación actualizada (original)'
                )

    def select_mod_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Seleccionar archivo modificado', '', 'Todos (*.*)')
        if file:
            self.show_preview(file, self.lbl_mod_preview)
            self.update_analysis_info(file, is_original=False)
            self.mod_file = file
            self.update_diff()
            # Registrar en historial si ambos archivos están seleccionados
            if hasattr(self, 'orig_file') and self.orig_file:
                self.add_history_entry(
                    'Análisis',
                    [self.orig_file, file],
                    'Comparación actualizada (modificado)'
                )

    def show_preview(self, file_path, label):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
            pixmap = QPixmap(file_path)
            label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio))
            label.setText('')
        elif ext in ['.wav', '.mp3']:
            try:
                from pydub.utils import mediainfo
                info = mediainfo(file_path)
                duration = float(info.get('duration', 0))
                duration_str = f"{duration:.1f} seg" if duration else "-"
            except Exception:
                duration_str = "-"
            label.setPixmap(QPixmap())
            label.setText(f'Audio: {os.path.basename(file_path)}\nDuración: {duration_str}')
        elif ext == '.pdf':
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(file_path)
                if reader.pages:
                    page = reader.pages[0]
                    text = page.extract_text()[:100] if page.extract_text() else "(Sin texto extraíble)"
                else:
                    text = "(PDF vacío)"
            except Exception:
                text = "(No se pudo leer PDF)"
            label.setPixmap(QPixmap())
            label.setText(f'PDF: {os.path.basename(file_path)}\nExtracto: {text}')
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
            'Imágenes (*.png *.jpg *.jpeg *.bmp);;Audio (*.wav *.mp3);;PDF (*.pdf);;Video (*.mp4 *.avi *.mov);;Word (*.docx);;ZIP (*.zip);;Todos (*.*)')
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
            'Imágenes (*.png *.jpg *.jpeg *.bmp);;Audio (*.wav *.mp3);;PDF (*.pdf);;Video (*.mp4 *.avi *.mov);;Word (*.docx);;ZIP (*.zip);;Todos (*.*)')
        for f in files:
            self.extract_carrier_list.addItem(f)

    def remove_extract_carrier(self):
        for item in self.extract_carrier_list.selectedItems():
            self.extract_carrier_list.takeItem(self.extract_carrier_list.row(item))

    def encode_files(self):
        if self.carrier_list.count() == 0 or self.secret_list.count() == 0:
            QMessageBox.warning(self, 'Datos Faltantes', 'Agrega al menos una portadora y uno o más archivos secretos.')
            return
        carrier = self.carrier_list.item(0).text()
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
        elif ext in ['.mp4', '.avi', '.mov']:
            file_filter = 'Video (*.mp4 *.avi *.mov);;Todos (*.*)'
        elif ext == '.docx':
            file_filter = 'Word (*.docx);;Todos (*.*)'
        elif ext == '.zip':
            file_filter = 'ZIP (*.zip);;Todos (*.*)'
        else:
            file_filter = 'Todos (*.*)'
        out_path, _ = QFileDialog.getSaveFileName(self, 'Guardar Portadora Modificada', '', file_filter)
        if not out_path:
            return
        try:
            self.progress.setVisible(True)
            self.progress.setValue(10)
            import hashlib
            orig_size = os.path.getsize(carrier)
            with open(carrier, 'rb') as f:
                orig_hash = hashlib.sha256(f.read()).hexdigest()
            self.lbl_orig_size.setText(f'Tamaño: {orig_size} bytes')
            self.lbl_orig_hash.setText(f'Hash SHA256: {orig_hash}')
            # Multi-archivo: empaquetar todos los archivos secretos
            payloads = []
            secret_files = []
            for i in range(self.secret_list.count()):
                secret = self.secret_list.item(i).text()
                secret_files.append(secret)
                with open(secret, 'rb') as f:
                    file_bytes = f.read()
                file_b64 = base64.b64encode(file_bytes).decode('utf-8')
                filename = os.path.basename(secret)
                payloads.append(filename + '||' + file_b64)
            # Unir todos los payloads con separador especial
            final_payload = '##MULTIFILE##'.join(payloads)
            # Cifrado avanzado si hay contraseña
            cipher_alg = self.cipher_combo.currentText()
            if pwd:
                final_payload = encrypt_message(final_payload, pwd, cipher_alg)
            self.progress.setValue(60)
            if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                ImageSteganography.encode(carrier, out_path, final_payload, password=pwd, is_binary=False)
            elif ext == '.wav':
                AudioSteganography.encode_wav(carrier, out_path, final_payload, password=pwd)
            elif ext == '.mp3':
                AudioSteganography.encode_mp3(carrier, out_path, final_payload, password=pwd)
            elif ext == '.pdf':
                PDFSteganography.encode(carrier, out_path, final_payload, password=pwd)
            elif ext == '.zip':
                ZipSteganography.encode(carrier, out_path, final_payload, password=pwd)
            elif ext == '.docx':
                DocxSteganography.encode(carrier, out_path, final_payload, password=pwd)
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
            QMessageBox.information(self, 'Éxito', f'Archivos ocultos exitosamente.\n\nGuardado: {os.path.basename(out_path)}')
            # Registrar en historial
            self.add_history_entry(
                'Ocultar',
                [carrier] + secret_files,
                f'Guardado: {os.path.basename(out_path)}'
            )
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al ocultar: {str(e)}')
            self.add_history_entry('Ocultar', [carrier], f'Error: {str(e)}')
        finally:
            self.progress.setVisible(False)

    def extract_files(self):
        if self.extract_carrier_list.count() == 0:
            QMessageBox.warning(self, 'Datos Faltantes', 'Selecciona una portadora para extraer.')
            return
        carrier = self.extract_carrier_list.item(0).text()
        pwd = self.extract_password.text() or None
        ext = os.path.splitext(carrier)[1].lower()
        extracted_files = []
        try:
            if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                payload = ImageSteganography.decode(carrier, password=pwd, is_binary=False)
            elif ext == '.wav':
                payload = AudioSteganography.decode_wav(carrier, password=pwd)
            elif ext == '.mp3':
                payload = AudioSteganography.decode_mp3(carrier, password=pwd)
            elif ext == '.pdf':
                payload = PDFSteganography.decode(carrier, password=pwd)
            elif ext == '.zip':
                payload = ZipSteganography.decode(carrier, password=pwd)
            elif ext == '.docx':
                payload = DocxSteganography.decode(carrier, password=pwd)
            else:
                raise Exception('Tipo de portadora no soportado.')
            # Descifrar si corresponde
            cipher_alg = getattr(self, 'cipher_combo', None)
            if pwd and cipher_alg:
                try:
                    payload = decrypt_message(payload, pwd, cipher_alg.currentText())
                except Exception:
                    pass
            # Multi-archivo: separar payloads
            if '##MULTIFILE##' in payload:
                parts = payload.split('##MULTIFILE##')
            else:
                parts = [payload]
            for part in parts:
                if '||' not in part:
                    continue
                header_end = part.find('||')
                if header_end == -1:
                    continue
                filename = part[:header_end]
                file_b64 = part[header_end+2:]
                file_bytes = base64.b64decode(file_b64)
                save_path, _ = QFileDialog.getSaveFileName(self, 'Guardar Archivo Extraído', filename)
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(file_bytes)
                    QMessageBox.information(self, 'Éxito', f'Archivo extraído: {os.path.basename(save_path)}')
                    extracted_files.append(save_path)
            # Registrar en historial
            self.add_history_entry(
                'Extraer',
                [carrier] + extracted_files,
                f'Extraídos: {len(extracted_files)} archivo(s)'
            )
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al extraer: {str(e)}')
            self.add_history_entry('Extraer', [carrier], f'Error: {str(e)}')

def main():
    app = QApplication(sys.argv)
    window = AdvancedSteganoGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()