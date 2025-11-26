
import numpy as np
from PIL import Image
from typing import Optional
import base64

class ImageSteganography:
    @staticmethod
    def encode(input_image_path: str, output_image_path: str, secret_data: str, password: Optional[str] = None, is_binary: bool = False) -> None:
        """
        Oculta datos (texto o binario, codificado en base64) en una imagen usando LSB.
        Si se proporciona una contraseña, los datos se cifran antes de ocultarlos.
        """
        image = Image.open(input_image_path)
        image = image.convert('RGB')
        data = np.array(image)
        flat_data = data.flatten()

        # Si es binario, secret_data debe ser base64
        if is_binary:
            message_bytes = base64.b64decode(secret_data)
            message_bin = ''.join([format(b, '08b') for b in message_bytes])
        else:
            if password:
                from src.utils.crypto import encrypt_message
                secret_data = encrypt_message(secret_data, password)
            # Codificar a base64 para robustez
            message_bytes = base64.b64encode(secret_data.encode('utf-8'))
            message_bin = ''.join([format(b, '08b') for b in message_bytes])

        message_bin += '1111111111111110'  # Marcador de fin

        if len(message_bin) > len(flat_data):
            raise ValueError('El mensaje/archivo es demasiado grande para esta imagen.')

        for i, bit in enumerate(message_bin):
            flat_data[i] = (flat_data[i] & 0xFE) | int(bit)

        new_data = flat_data.reshape(data.shape)
        new_image = Image.fromarray(new_data.astype('uint8'), 'RGB')
        new_image.save(output_image_path)

    @staticmethod
    def decode(stego_image_path: str, password: Optional[str] = None, is_binary: bool = False) -> str:
        """
        Extrae datos ocultos de una imagen. Si se usó contraseña, descifra el mensaje.
        Si is_binary=True, retorna base64 del archivo binario.
        """
        image = Image.open(stego_image_path)
        image = image.convert('RGB')
        data = np.array(image)
        flat_data = data.flatten()
        bits = []
        for value in flat_data:
            bits.append(str(value & 1))
        # Buscar marcador de fin
        message_bin = ''.join(bits)
        end_marker = '1111111111111110'
        end_idx = message_bin.find(end_marker)
        if end_idx == -1:
            raise ValueError('No se encontró mensaje oculto.')
        message_bin = message_bin[:end_idx]
        # Convertir binario a bytes
        message_bytes = bytearray()
        for i in range(0, len(message_bin), 8):
            byte = message_bin[i:i+8]
            if len(byte) == 8:
                message_bytes.append(int(byte, 2))
        if is_binary:
            # Retornar base64 para reconstruir archivo
            return base64.b64encode(message_bytes).decode('utf-8')
        else:
            # Decodificar base64 a texto
            try:
                decoded = base64.b64decode(message_bytes).decode('utf-8')
            except Exception:
                decoded = base64.b64decode(message_bytes)
            if password:
                from src.utils.crypto import decrypt_message
                decoded = decrypt_message(decoded, password)
            return decoded
