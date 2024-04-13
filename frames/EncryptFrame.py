import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from config import KEY_EXTENSION, FILE_EXTENSION

class EncryptFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename = tk.StringVar()
        self.keyname = tk.StringVar()
        self.key_path = None
        self.file_path = None
        tk.Label(self, text="Encrypt").pack(pady=10)
        
        tk.Button(self, text="Select file", command=self._select_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.filename).pack()
        
        tk.Button(self, text="Select key", command=self._select_key).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.keyname).pack()
        
        tk.Button(self, text="Encrypt", command=self._encrypt).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack(fill=tk.X, padx=50, pady=5)
        
    def _select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path and self.controller.check_extension(self.file_path, FILE_EXTENSION):  # Check if a file was actually selected
            self.filename.set("File path:\n" + self.file_path) # TODO zrobic z tego metode w appcontroller
        
    def _select_key(self):
        self.key_path = filedialog.askopenfilename()
        if self.key_path and self.controller.check_extension(self.key_path, KEY_EXTENSION):  # Check if a file was actually selected
            self.keyname.set("Key path:\n" + self.key_path)
    
    def _encrypt(self):
        if self.key_path and self.file_path:
            messagebox.showinfo("Info", "File encrypted successfully")
        else:
            messagebox.showerror("Error", "Select file and key first")            
