import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import PKCS1_OAEP
from config import FILE_EXTENSION

class DecryptFrame(tk.Frame):
    """
    A frame that provides functionality for decrypting files using a private key loaded from an external device.
    This frame allows users to select encrypted files, detect and load the private key, and enter a PIN for decryption.
    """
    
    def __init__(self, parent, controller):
        """
        Initialize the Decrypt frame within the parent container.

        Args:
            parent (tk.Widget): The parent widget in which this frame will be placed.
            controller (object): The main application controller which manages navigation between frames.
        """
        super().__init__(parent)
        self.controller = controller
        self.key_path = None
        self.file_path = None
        self.pin = None

        # GUI elements setup
        self.pinname = tk.StringVar()
        self.filename = tk.StringVar()
        self.keyname = tk.StringVar()

        # UI layout for the decryption frame
        tk.Label(self, text="Decrypt").pack(pady=10)
        tk.Button(self, text="Select file", command=self._select_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.filename).pack()

        tk.Button(self, text="Find device", command=self._find_device).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.keyname).pack()

        tk.Label(self, text="Enter the PIN").pack()
        self.pin_entry = tk.Entry(self, textvariable=self.pinname, show="*", width=4)
        self.pin_entry.pack(pady=5)

        tk.Button(self, text="Decrypt", command=self._decrypt_controller).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack(fill=tk.X, padx=50, pady=5)
    
    def _select_file(self):
        """Selects an encrypted file for decryption."""
        self.file_path = self.controller.select_file(extensions=FILE_EXTENSION)
        self.filename.set(f"File:\n{self.file_path}")
        
    def _find_device(self):
        """Finds an external device and loads the private key if available."""
        mountpoint = self.controller.check_external_storage()
        if mountpoint:
            self.key_path = self.controller.check_private_key_on_external_storage(mountpoint)
            if self.key_path:
                self.keyname.set(f"Key:\n{self.key_path}")
            else:
                messagebox.showerror("Error", "No private key found on external storage")
        else:
            messagebox.showerror("Error", "No external storage found")
            
    def _decrypt_controller(self):
        """
        Controller method that manages the decryption process,
        including validation of inputs and reporting of decryption status.
        """
        if self.key_path and self.file_path and self.controller.check_pin(self.pin_entry.get()):
            if self._decrypt():
                messagebox.showinfo("Info", "File decrypted successfully")
                self._clear_variables()
            else:
                messagebox.showerror("Error", "Failed to decrypt the private key")
        else:
            messagebox.showerror("Error", "Select file, type PIN and put pendrive with private key first")    

    def _decrypt(self):
        """
        Performs the decryption of the selected file using the loaded private key.

        Returns:
            bool: True if the decryption was successful, otherwise False.
        """
        try:
            with open(self.file_path, "rb") as file:
                file_content = file.read()

            private_key = self.controller.decrypt_private_key(self.pin_entry.get(), self.key_path)
            if private_key is None:
                return False
            
            cipher = PKCS1_OAEP.new(private_key)
            decrypted_content = cipher.decrypt(file_content)

            with open(self.file_path, "wb") as file:
                file.write(decrypted_content)
            return True
        except Exception as e:
            print(f"Decryption failed: {e}")
            return False
        
    def _clear_variables(self):
        """Clears all input variables and resets the frame to its initial state."""
        self.filename.set("")
        self.keyname.set("")
        self.pinname.set("")
        self.file_path = None
        self.key_path = None
