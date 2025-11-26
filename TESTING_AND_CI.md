# Pruebas automáticas y CI/CD para Esteganografía Avanzada

Este archivo describe cómo agregar pruebas automáticas y un pipeline básico de CI/CD usando GitHub Actions y pytest.

## 1. Estructura recomendada de tests

- Crea una carpeta `tests/` en la raíz del proyecto.
- Dentro, crea archivos como `test_image.py`, `test_audio.py`, `test_pdf.py`, etc.
- Ejemplo de test básico (tests/test_image.py):

```python
import pytest
from src.steganografia.image import ImageSteganography

def test_encode_decode_image(tmp_path):
    # Prepara una imagen de prueba y un mensaje
    img_path = tmp_path / "test.png"
    # ...código para crear imagen dummy...
    # ...código para ocultar y extraer mensaje...
    # assert mensaje extraído == mensaje original
    pass  # Implementar
```

## 2. Instalación de pytest

En tu entorno:
    pip install pytest

## 3. Ejecutar pruebas localmente

pytest

## 4. Configuración de CI/CD (GitHub Actions)

Crea `.github/workflows/python-app.yml` con:

```yaml
name: Python application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest
    - name: Run tests
      run: pytest
```

## 5. Consejos

- Agrega tests para cada módulo de esteganografía y cifrado.
- Usa `tmp_path` de pytest para archivos temporales.
- Puedes agregar cobertura con `pytest-cov`.

---

Esto te permitirá validar automáticamente cada push/pull request y mantener la calidad del proyecto.
