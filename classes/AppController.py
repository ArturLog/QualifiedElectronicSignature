import tkinter as tk
import hashlib
import os
import psutil
from tkinter import messagebox
from tkinter import filedialog
from frames.MainFrame import MainFrame
from frames.SignDocumentFrame import SignDocumentFrame
from frames.VerifySignatureFrame import VerifySignatureFrame
from frames.EncryptFrame import EncryptFrame
from frames.DecryptFrame import DecryptFrame
from frames.AboutUsFrame import AboutUsFrame
from Crypto.PublicKey import RSA 
from Crypto.Cipher import AES
from config import *

class AppController(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title(DEFAULT_TITLE)
        self.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
        
        self.frames = {}
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initializing all frames
        for F in (MainFrame, SignDocumentFrame, VerifySignatureFrame, EncryptFrame, DecryptFrame, AboutUsFrame):
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainFrame")

    def select_file(self, extensions=["txt"]):
        file_path = filedialog.askopenfilename()
        if file_path and self.check_extension(file_path, extensions):
            return file_path
        return ""

    def show_frame(self, frame_name):
        '''Show a frame for the given frame name'''
        frame = self.frames[frame_name]
        frame.tkraise()
    
    def check_extension(self, file_path ,extensions):
        if file_path.split('.')[-1] not in extensions:
            messagebox.showerror("Error", "Invalid file extension")
            return False
        return True
    
    def check_external_storage(self):
        partitions = psutil.disk_partitions(all=True)
        for partition in partitions:
            if 'removable' in partition.opts:
                if os.path.exists(partition.mountpoint):
                    return partition.mountpoint
        return None
    
    def check_private_key_on_external_storage(self, mountpoint):
        files = os.listdir(mountpoint)
        for file in files:
            if file.endswith(".pem"):
                return os.path.join(mountpoint, file)
        return None
    
    def decrypt_private_key(self, pin, key_path):
        with open(key_path, "rb") as f:
            encrypted_key = f.read()
            
        iv = encrypted_key[:AES.block_size]
        encrypted_key = encrypted_key[AES.block_size:]

        key = hashlib.sha256(pin.encode()).digest()
        cipher = AES.new(key, AES.MODE_CFB, iv)
        decrypted_key = cipher.decrypt(encrypted_key)
        try:
            return RSA.import_key(decrypted_key)
        except Exception as e:
            print(e)
            return None
    
    def check_pin(self, pin):
        if not pin:
            messagebox.showerror("Error", "Type PIN first")
            return False
        elif len(pin) != PIN_LENGHT or not pin.isdigit():
            messagebox.showerror("Error", f"PIN must be exactly {PIN_LENGHT} digits")
            return False
        return True