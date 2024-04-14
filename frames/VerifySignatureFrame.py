import tkinter as tk
from tkinter import messagebox
from config import KEY_EXTENSION, FILE_EXTENSION

class VerifySignatureFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename = tk.StringVar()
        self.keyname = tk.StringVar()
        tk.Label(self, text="Verify signature").pack(pady=10)
        
        tk.Button(self, text="Select file", command=self._select_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.filename).pack()
        
        tk.Button(self, text="Select public key", command=self._select_key).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.keyname).pack()
        
        tk.Button(self, text="Verify", command=self._verify).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack(fill=tk.X, padx=50, pady=5)
        
    def _select_file(self):
        self.filename.set("File:\n" + self.controller.select_file(extensions=FILE_EXTENSION))
        
    def _select_key(self):
        self.keyname.set("Key:\n" + self.controller.select_file(extensions=KEY_EXTENSION))
    
    def _verify(self):
        if '.' in self.filename.get() and '.' in self.keyname.get():
            messagebox.showinfo("Info", "File verified successfully")
            self.filename.set("")
            self.keyname.set("")
        else:
            messagebox.showerror("Error", "Select file and key first")           
