
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sys
import pathlib
import os
# Añadir la raíz del proyecto al sys.path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))
from src.steganografia.image import ImageSteganography

class SteganoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Esteganografía Visual')
        self.image_path = None
        self.stego_path = None
        self.img_label = tk.Label(root)
        self.img_label.pack()
        
        frame = tk.Frame(root)
        frame.pack(pady=10)
        tk.Button(frame, text='Cargar Imagen', command=self.load_image).grid(row=0, column=0, padx=5)
        tk.Button(frame, text='Ocultar Mensaje', command=self.encode_message).grid(row=0, column=1, padx=5)
        tk.Button(frame, text='Extraer Mensaje', command=self.decode_message).grid(row=0, column=2, padx=5)
        
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack(pady=5)
        self.password_entry = tk.Entry(root, width=30, show='*')
        self.password_entry.pack(pady=5)
        self.status = tk.Label(root, text='')
        self.status.pack()

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[('Imagen', '*.png;*.jpg;*.jpeg;*.bmp')])
        if path:
            self.image_path = path
            img = Image.open(path)
            img.thumbnail((300, 300))
            self.tk_img = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.tk_img)
            self.status.config(text=f'Imagen cargada: {os.path.basename(path)}')

    def encode_message(self):
        if not self.image_path:
            messagebox.showerror('Error', 'Primero carga una imagen.')
            return
        msg = self.message_entry.get()
        pwd = self.password_entry.get() or None
        out_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG', '*.png')])
        if not out_path:
            return
        try:
            ImageSteganography.encode(self.image_path, out_path, msg, pwd)
            self.status.config(text='Mensaje oculto correctamente.')
            messagebox.showinfo('Éxito', 'Mensaje oculto en la imagen.')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def decode_message(self):
        path = filedialog.askopenfilename(filetypes=[('Imagen', '*.png;*.jpg;*.jpeg;*.bmp')])
        if not path:
            return
        pwd = self.password_entry.get() or None
        try:
            msg = ImageSteganography.decode(path, pwd)
            self.status.config(text='Mensaje extraído.')
            messagebox.showinfo('Mensaje extraído', msg)
        except Exception as e:
            messagebox.showerror('Error', str(e))

def main():
    root = tk.Tk()
    app = SteganoGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
