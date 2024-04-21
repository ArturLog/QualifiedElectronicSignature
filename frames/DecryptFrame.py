import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import PKCS1_OAEP
from config import FILE_EXTENSION

class DecryptFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.key_path = None
        self.file_path = None
        self.pin = None
        self.filename = tk.StringVar()
        self.keyname = tk.StringVar()
        tk.Label(self, text="Decrypt").pack(pady=10)
        
        tk.Button(self, text="Select file", command=self._select_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.filename).pack()
        
        tk.Button(self, text="Find device", command=self._find_device).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.keyname).pack()
        
        tk.Label(self, textvariable="Enter the PIN").pack()
        self.pin_entry = tk.Entry(self, show="*", width=4)
        self.pin_entry.pack(pady=5)
        
        tk.Button(self, text="Decrypt", command=self._decrypt_controller).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack(fill=tk.X, padx=50, pady=5)
    
    def _select_file(self):
        self.file_path = self.controller.select_file(extensions=FILE_EXTENSION)
        self.filename.set("File:\n" + self.file_path)
        
    def _find_device(self):
        mountpoint = self.controller.check_external_storage()
        if mountpoint:
            self.key_path = self.controller.check_private_key_on_external_storage(mountpoint)
            if self.key_path:
                self.keyname.set("Key:\n" + self.key_path)
            else:
                messagebox.showerror("Error", "No private key found on external storage")
        else:
            messagebox.showerror("Error", "No external storage found")
            
    def _decrypt_controller(self):
        if self.key_path and self.file_path and self._check_pin():
            if self._decrypt():
                messagebox.showinfo("Info", "File decrypted successfully")
                self._clear_paths()
            else:
                messagebox.showerror("Error", "Failed to decrypt the private key")
        else:
            messagebox.showerror("Error", "Select file, type PIN and put pendrive with private key first")    
    
    def _check_pin(self):
        self.pin = self.pin_entry.get()
        if not self.pin:
            messagebox.showerror("Error", "Type PIN first")
            return False
        elif len(self.pin) != 4 or not self.pin.isdigit():
            messagebox.showerror("Error", "PIN must be exactly 4 digits")
            return False
        return True
    
    def _decrypt(self):
        with open(self.file_path, "rb") as file:
            file_content = file.read()
        
        private_key = self.controller.decrypt_private_key(self.pin, self.key_path)
        if private_key is None:
            return False
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_content = cipher.decrypt(file_content)
        with open(self.file_path, "wb") as file:
            file.write(decrypted_content)
        return True
        
    
    def _clear_paths(self):
        self.filename.set("")
        self.keyname.set("")
        self.file_path = None
        self.key_path = None     
        self.pin = None
    
