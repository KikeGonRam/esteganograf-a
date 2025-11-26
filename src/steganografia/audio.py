import wave
import os
import base64
from typing import Optional
from pydub import AudioSegment

class AudioSteganography:
    @staticmethod
    def encode_wav(input_audio_path: str, output_audio_path: str, secret_data: str, password: Optional[str] = None) -> None:
        # Codifica datos en base64 y oculta en LSB de un archivo WAV
        with wave.open(input_audio_path, 'rb') as audio:
            params = audio.getparams()
            frames = bytearray(list(audio.readframes(audio.getnframes())))
        # Cifrado opcional
        if password:
            from src.utils.crypto import encrypt_message
            secret_data = encrypt_message(secret_data, password)
        data_bytes = base64.b64encode(secret_data.encode('utf-8'))
        data_bin = ''.join([format(b, '08b') for b in data_bytes])
        data_bin += '1111111111111110'  # Marcador de fin
        if len(data_bin) > len(frames):
            raise ValueError('El mensaje es demasiado grande para este audio.')
        for i, bit in enumerate(data_bin):
            frames[i] = (frames[i] & 0xFE) | int(bit)
        with wave.open(output_audio_path, 'wb') as audio_out:
            audio_out.setparams(params)
            audio_out.writeframes(bytes(frames))

    @staticmethod
    def decode_wav(stego_audio_path: str, password: Optional[str] = None) -> str:
        with wave.open(stego_audio_path, 'rb') as audio:
            frames = bytearray(list(audio.readframes(audio.getnframes())))
        bits = [str(f & 1) for f in frames]
        data_bin = ''.join(bits)
        end_marker = '1111111111111110'
        end_idx = data_bin.find(end_marker)
        if end_idx == -1:
            raise ValueError('No se encontró mensaje oculto.')
        data_bin = data_bin[:end_idx]
        data_bytes = bytearray()
        for i in range(0, len(data_bin), 8):
            byte = data_bin[i:i+8]
            if len(byte) == 8:
                data_bytes.append(int(byte, 2))
        decoded = base64.b64decode(data_bytes).decode('utf-8')
        if password:
            from src.utils.crypto import decrypt_message
            decoded = decrypt_message(decoded, password)
        return decoded

    @staticmethod
    def encode_mp3(input_audio_path: str, output_audio_path: str, secret_data: str, password: Optional[str] = None) -> None:
        # Convertir MP3 a WAV, ocultar, luego volver a MP3
        temp_wav = 'temp_steg.wav'
        audio = AudioSegment.from_mp3(input_audio_path)
        audio.export(temp_wav, format='wav')
        AudioSteganography.encode_wav(temp_wav, temp_wav, secret_data, password)
        AudioSegment.from_wav(temp_wav).export(output_audio_path, format='mp3')
        os.remove(temp_wav)

    @staticmethod
    def decode_mp3(stego_audio_path: str, password: Optional[str] = None) -> str:
        # Convertir MP3 a WAV y extraer
        temp_wav = 'temp_steg.wav'
        audio = AudioSegment.from_mp3(stego_audio_path)
        audio.export(temp_wav, format='wav')
        result = AudioSteganography.decode_wav(temp_wav, password)
        os.remove(temp_wav)
        return result
