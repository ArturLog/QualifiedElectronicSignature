import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from config import KEY_EXTENSION, FILE_EXTENSION

class DecryptFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename = tk.StringVar()
        self.keyname = tk.StringVar()
        self.key_path = None
        self.file_path = None
        tk.Label(self, text="Decrypt").pack(pady=10)
        
        #tk.Button(self, text="Select file", command=self._select_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.filename).pack()
        
        # check pendrive
        #tk.Button(self, text="Select key", command=self._select_key).pack(fill=tk.X, padx=50, pady=5)
        #tk.Label(self, textvariable=self.keyname).pack()
        
        #tk.Button(self, text="Decrypt", command=self._encrypt).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack(fill=tk.X, padx=50, pady=5)
        
    def _decrypt(self):
        if self.key_path and self.file_path:
            messagebox.showinfo("Info", "File decrypted successfully")
        else:
            messagebox.showerror("Error", "Select file and put pendrive with private key first")    