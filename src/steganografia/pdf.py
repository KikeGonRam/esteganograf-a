import PyPDF2
import base64
import os
from typing import Optional

class PDFSteganography:
    @staticmethod
    def encode(input_pdf_path: str, output_pdf_path: str, secret_data: str, password: Optional[str] = None) -> None:
        # Codifica datos en base64 y los inserta como metadato personalizado en el PDF
        with open(input_pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            writer = PyPDF2.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            # Cifrado opcional
            if password:
                from src.utils.crypto import encrypt_message
                secret_data = encrypt_message(secret_data, password)
            data_b64 = base64.b64encode(secret_data.encode('utf-8')).decode('utf-8')
            # Insertar como metadato personalizado
            metadata = reader.metadata or {}
            metadata = dict(metadata)
            metadata['/HiddenData'] = data_b64
            writer.add_metadata(metadata)
            with open(output_pdf_path, 'wb') as out_f:
                writer.write(out_f)

    @staticmethod
    def decode(stego_pdf_path: str, password: Optional[str] = None) -> str:
        with open(stego_pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            metadata = reader.metadata
            if not metadata or '/HiddenData' not in metadata:
                raise ValueError('No se encontró mensaje oculto en el PDF.')
            data_b64 = metadata['/HiddenData']
            decoded = base64.b64decode(data_b64).decode('utf-8')
            if password:
                from src.utils.crypto import decrypt_message
                decoded = decrypt_message(decoded, password)
            return decoded
