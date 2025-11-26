import zipfile
import base64
import os

class ZipSteganography:
    @staticmethod
    def encode(carrier_path, out_path, payload, password=None):
        # Oculta el payload como un archivo oculto dentro de un ZIP
        with zipfile.ZipFile(carrier_path, 'r') as zin:
            with zipfile.ZipFile(out_path, 'w') as zout:
                # Copiar archivos originales
                for item in zin.infolist():
                    buffer = zin.read(item.filename)
                    zout.writestr(item, buffer)
                # Agregar el payload como archivo oculto
                zout.writestr('.hidden_payload', base64.b64encode(payload.encode('utf-8')))

    @staticmethod
    def decode(carrier_path, password=None):
        # Extrae el payload oculto de un ZIP
        with zipfile.ZipFile(carrier_path, 'r') as z:
            if '.hidden_payload' in z.namelist():
                data = z.read('.hidden_payload')
                return base64.b64decode(data).decode('utf-8')
            else:
                raise Exception('No se encontró información oculta en el ZIP')
