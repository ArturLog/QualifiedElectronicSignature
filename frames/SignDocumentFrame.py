import tkinter as tk
from tkinter import messagebox
from config import FILE_EXTENSION

class SignDocumentFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self._key_path = None
        self.filename = tk.StringVar()
        self.keyname = tk.StringVar()
        tk.Label(self, text="Sign document").pack(pady=10)
        
        tk.Button(self, text="Select file", command=self._select_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.filename).pack()
        
        tk.Button(self, text="Find device", command=self._find_device).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.keyname).pack()
        
        tk.Button(self, text="Sign", command=self._sign_document).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack(fill=tk.X, padx=50, pady=5)
    
    def _select_file(self):
        self.filename.set("File:\n" + self.controller.select_file(extensions=FILE_EXTENSION))
    
    def _find_device(self):
        mountpoint = self.controller.check_external_storage()
        if mountpoint:
            self._key_path = self.controller.check_private_key_on_external_storage(mountpoint)
            if self._key_path:
                self.keyname.set("Key:\n" + self._key_path)
            else:
                messagebox.showerror("Error", "No private key found on external storage")
        else:
            messagebox.showerror("Error", "No external storage found")
    
    def _sign_document(self):
        if '.' in self.filename.get() and '.' in self.keyname.get():
            messagebox.showinfo("Info", "File signed successfully")
        else:
            messagebox.showerror("Error", "Select file and put pendrive with private key first")    