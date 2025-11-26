import numpy as np
from PIL import Image
from typing import Optional

class ImageSteganography:
    @staticmethod
    def encode(input_image_path: str, output_image_path: str, secret_message: str, password: Optional[str] = None) -> None:
        """
        Oculta un mensaje de texto en una imagen usando LSB (Least Significant Bit).
        Si se proporciona una contraseña, el mensaje se cifra antes de ocultarlo.
        """
        image = Image.open(input_image_path)
        image = image.convert('RGB')
        data = np.array(image)
        flat_data = data.flatten()
        
        # Convertir mensaje a binario
        if password:
            from src.utils.crypto import encrypt_message
            secret_message = encrypt_message(secret_message, password)
        message_bin = ''.join([format(ord(c), '08b') for c in secret_message])
        message_bin += '1111111111111110'  # Marcador de fin
        
        if len(message_bin) > len(flat_data):
            raise ValueError('El mensaje es demasiado largo para esta imagen.')
        
        for i, bit in enumerate(message_bin):
            flat_data[i] = (flat_data[i] & 0xFE) | int(bit)
        
        new_data = flat_data.reshape(data.shape)
        new_image = Image.fromarray(new_data.astype('uint8'), 'RGB')
        new_image.save(output_image_path)

    @staticmethod
    def decode(stego_image_path: str, password: Optional[str] = None) -> str:
        """
        Extrae un mensaje oculto de una imagen. Si se usó contraseña, descifra el mensaje.
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
        chars = [chr(int(message_bin[i:i+8], 2)) for i in range(0, len(message_bin), 8)]
        message = ''.join(chars)
        if password:
            from src.utils.crypto import decrypt_message
            message = decrypt_message(message, password)
        return message
