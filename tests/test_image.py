import pytest
from src.steganografia.image import ImageSteganography
from PIL import Image
import tempfile
import os

def test_encode_decode_image(tmp_path):
    # Crear imagen dummy
    img_path = tmp_path / "test.png"
    img = Image.new('RGB', (100, 100), color='white')
    img.save(img_path)
    mensaje = "Mensaje secreto de prueba"
    # Codificar mensaje
    out_path = tmp_path / "out.png"
    ImageSteganography.encode(str(img_path), str(out_path), mensaje)
    # Decodificar mensaje
    extraido = ImageSteganography.decode(str(out_path))
    assert extraido == mensaje
