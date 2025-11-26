from setuptools import setup, find_packages

setup(
    name='steganografia_avanzada',
    version='0.1.0',
    description='Proyecto avanzado de esteganografía en imágenes, audio y video',
    author='Tu Nombre',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'opencv-python',
        'pillow',
        'cryptography',
        'click',
        'scipy',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'stegano-cli=src.cli:main',
        ],
    },
)
