# Instrucciones para crear un instalador y ejecutable standalone

## 1. Requisitos previos

- Python 3.12 instalado
- Instala PyInstaller en tu entorno:

    pip install pyinstaller

## 2. Comando básico para generar el ejecutable

Desde la raíz del proyecto, ejecuta:

    pyinstaller --noconfirm --onefile --windowed --icon=icon.ico src/steganografia/gui_advanced.py

- `--onefile`: genera un solo archivo ejecutable.
- `--windowed`: sin consola (para apps GUI).
- `--icon=icon.ico`: opcional, usa tu propio icono.

## 3. Archivos de recursos y dependencias

- Si usas archivos de traducción (.qm), iconos, imágenes, etc., agrégalos con:

    --add-data "ruta\al\archivo;destino_relativo"

Ejemplo:

    --add-data "src\steganografia\en.qm;steganografia"

Puedes agregar varios `--add-data`.

## 4. Salida

- El ejecutable estará en `dist/gui_advanced.exe`.

## 5. Instalador (opcional)

- Para crear un instalador profesional, usa Inno Setup (Windows) o NSIS.
- Exporta el ejecutable y recursos necesarios, y sigue el asistente del creador de instaladores.

## 6. Consejos

- Prueba el ejecutable en una carpeta limpia.
- Si usas ffmpeg, pydub, etc., asegúrate de incluir los binarios necesarios.

---

Puedes personalizar el nombre del ejecutable con `--name "EsteganografiaPro"`.

Para soporte multiplataforma, repite el proceso en cada SO.
