import tkinter as tk
from tkinter import messagebox
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from config import KEY_EXTENSION, FILE_EXTENSION

class EncryptFrame(tk.Frame):
    """
    A frame that provides functionality for encrypting files using a public key.
    Users can select a file to encrypt and a public key, and then perform the encryption.
    """
    
    def __init__(self, parent, controller):
        """
        Initialize the Encrypt frame within the parent container.

        Args:
            parent (tk.Widget): The parent widget in which this frame will be placed.
            controller (object): The main application controller which manages navigation between frames.
        """
        super().__init__(parent)
        self.controller = controller
        self.file_path = None
        self.key_path = None

        # Variables to store the path names in the UI
        self.filename = tk.StringVar()
        self.keyname = tk.StringVar()

        # UI layout for the encryption frame
        tk.Label(self, text="Encrypt").pack(pady=10)
        tk.Button(self, text="Select file", command=self._select_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.filename).pack()

        tk.Button(self, text="Select public key", command=self._select_key).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.keyname).pack()

        tk.Button(self, text="Encrypt", command=self._encrypt_controller).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack(fill=tk.X, padx=50, pady=5)
    
    def _select_file(self):
        """Selects a file for encryption and updates the filename variable in the UI."""
        self.file_path = self.controller.select_file(extensions=FILE_EXTENSION)
        self.filename.set(f"File:\n{self.file_path}")
        
    def _select_key(self):
        """Selects a public key for encryption and updates the keyname variable in the UI."""
        self.key_path = self.controller.select_file(extensions=KEY_EXTENSION)
        self.keyname.set(f"Key:\n{self.key_path}")
    
    def _encrypt_controller(self):
        """
        Controller method that manages the encryption process,
        including validation of inputs and reporting of encryption status.
        """
        if self.key_path and self.file_path:
            if self._encrypt():
                messagebox.showinfo("Info", "File encrypted successfully")
                self._clear_variables()
            else:
                messagebox.showerror("Error", "File encryption failed")
        else:
            messagebox.showerror("Error", "Select file and key first")       
    
    def _encrypt(self):
        """
        Performs the encryption of the selected file using the loaded public key.

        Returns:
            bool: True if the encryption was successful, otherwise False.
        """
        try:
            with open(self.file_path, "rb") as file:
                file_content = file.read()
            with open(self.key_path, "r") as key_file:
                public_key = RSA.import_key(key_file.read())

            cipher_rsa = PKCS1_OAEP.new(public_key)
            encrypted_content = cipher_rsa.encrypt(file_content)

            with open(self.file_path, "wb") as file:
                file.write(encrypted_content)
            return True
        except Exception as e:
            print(f"Encryption failed: {e}")
            return False
    
    def _clear_variables(self):
        """Clears all input variables and resets the frame to its initial state."""
        self.filename.set("")
        self.keyname.set("")
        self.file_path = None
        self.key_path = None     
