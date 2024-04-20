import tkinter as tk
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from tkinter import messagebox
from config import KEY_EXTENSION, FILE_EXTENSION

class EncryptFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.file_path = None
        self.key_path = None
        self.filename = tk.StringVar()
        self.keyname = tk.StringVar()
        tk.Label(self, text="Encrypt").pack(pady=10)
        
        tk.Button(self, text="Select file", command=self._select_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.filename).pack()
        
        tk.Button(self, text="Select public key", command=self._select_key).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.keyname).pack()
        
        tk.Button(self, text="Encrypt", command=self._encrypt_controller).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack(fill=tk.X, padx=50, pady=5)
        
    def _select_file(self):
        self.file_path = self.controller.select_file(extensions=FILE_EXTENSION)
        self.filename.set("File:\n" + self.file_path)
        
    def _select_key(self):
        self.key_path = self.controller.select_file(extensions=KEY_EXTENSION)
        self.keyname.set("Key:\n" + self.key_path)
    
    def _encrypt_controller(self):
        if self.key_path and self.file_path:
            self._encrypt()
            messagebox.showinfo("Info", "File encrypted successfully")
            self._clear_paths()
        else:
            messagebox.showerror("Error", "Select file and key first")       
    
    def _encrypt(self):
        with open(self.file_path, "rb") as file:
            file_content = file.read()
        with open(self.key_path, "r") as key:
            public_key = RSA.import_key(key.read())
                
        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted_content = cipher_rsa.encrypt(file_content)
            
        with open(self.file_path, "wb") as file:
            file.write(encrypted_content)
    
    def _clear_paths(self):
        self.filename.set("")
        self.keyname.set("")
        self.file_path = None
        self.key_path = None     
