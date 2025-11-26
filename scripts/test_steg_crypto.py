
import os
import sys
import pathlib
# Añadir la raíz del proyecto al sys.path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from src.utils.crypto import encrypt_message, decrypt_message
from src.steganografia.image import ImageSteganography
from PIL import Image
import numpy as np

def create_sample_image(path):
    # Crea una imagen RGB pequeña para pruebas
    data = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    img = Image.fromarray(data, 'RGB')
    img.save(path)

def test_crypto():
    mensaje = 'Mensaje secreto'
    password = 'clave123'
    cifrado = encrypt_message(mensaje, password)
    descifrado = decrypt_message(cifrado, password)
    print('Original:', mensaje)
    print('Cifrado:', cifrado)
    print('Descifrado:', descifrado)
    assert mensaje == descifrado

def test_steganografia():
    img_in = 'test_input.png'
    img_out = 'test_output.png'
    mensaje = 'Oculto en imagen'
    password = 'clave123'
    create_sample_image(img_in)
    ImageSteganography.encode(img_in, img_out, mensaje, password)
    extraido = ImageSteganography.decode(img_out, password)
    print('Mensaje oculto:', mensaje)
    print('Mensaje extraído:', extraido)
    assert mensaje == extraido
    os.remove(img_in)
    os.remove(img_out)

if __name__ == '__main__':
    print('--- Prueba de cifrado ---')
    test_crypto()
    print('--- Prueba de esteganografía en imagen ---')
    test_steganografia()
