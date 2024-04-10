import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class EncryptFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename = ""
        self.keyname = ""
        tk.Label(self, text="Encrypt").pack(pady=10)
        tk.Button(self, text="Select file", command=self._select_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, text="File path:\n" + self.filename).pack()
        tk.Button(self, text="Select key", command=self._select_key).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, text="Key path:\n" + self.keyname).pack()
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack(fill=tk.X, padx=50, pady=5)
        
    def _select_file(self):
        self.filename = filedialog.askopenfilename()
        
    def _select_key(self):
        self.keyname = filedialog.askopenfilename()
        
    def _check_format(self, formatlist):
        pass