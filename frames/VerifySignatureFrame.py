import tkinter as tk
from lxml import etree
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from tkinter import messagebox
from config import KEY_EXTENSION, FILE_EXTENSION, SIGNATURE_EXTENSION

class VerifySignatureFrame(tk.Frame):
    """
    A frame for verifying the signature of a document using a corresponding public key.
    This frame allows the user to select a document, its associated signature file, and the public key
    to perform the verification process.
    """
    
    def __init__(self, parent, controller):
        """
        Initialize the Verify Signature frame within the parent container.

        Args:
            parent (tk.Widget): The parent widget in which this frame will be placed.
            controller (object): The main application controller which manages navigation between frames.
        """
        super().__init__(parent)
        self.controller = controller
        self.signature_path = None
        self.file_path = None
        self.key_path = None
        self.filename = tk.StringVar()
        self.keyname = tk.StringVar()
        self.signaturename = tk.StringVar()

        # UI setup for signature verification
        tk.Label(self, text="Verify signature").pack(pady=10)
        tk.Button(self, text="Select file", command=self._select_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.filename).pack()
        
        tk.Button(self, text="Select public key", command=self._select_key).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.keyname).pack()
        
        tk.Button(self, text="Select the signature", command=self._select_signature).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.signaturename).pack()
        
        tk.Button(self, text="Verify", command=self._verify_controller).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack(fill=tk.X, padx=50, pady=5)
        
    def _select_file(self):
        """Selects a file for which the signature needs to be verified and updates the filename variable."""
        self.file_path = self.controller.select_file(extensions=FILE_EXTENSION)
        self.filename.set(f"File:\n{self.file_path}")
        
    def _select_key(self):
        """Selects a public key file for verifying the signature and updates the keyname variable."""
        self.key_path = self.controller.select_file(extensions=KEY_EXTENSION)
        self.keyname.set(f"Key:\n{self.key_path}")
        
    def _select_signature(self):
        """Selects a signature file and updates the signaturename variable."""
        self.signature_path = self.controller.select_file(extensions=SIGNATURE_EXTENSION)
        self.signaturename.set(f"Signature:\n{self.signature_path}")
    
    def _verify_controller(self):
        """
        Controller method that manages the signature verification process,
        including validation of inputs and reporting of the verification status.
        """
        if self.key_path and self.file_path and self.signature_path:
            if self._verify():
                messagebox.showinfo("Info", "File verified successfully")
                self._clear_variables()
            else:
                messagebox.showerror("Error", "File verification failed")
        else:
            messagebox.showerror("Error", "Select file, key, and signature first")
    
    def _verify(self):
        """
        Performs the signature verification using the public key, file content, and signature.

        Returns:
            bool: True if the signature is valid, otherwise False.
        """
        try:
            with open(self.file_path, "rb") as file:
                file_content = file.read()
            with open(self.key_path, "r") as key_file:
                public_key = RSA.import_key(key_file.read())
            with open(self.signature_path, 'rb') as sig_file:
                signature_tree = etree.parse(sig_file)

            # Retrieve the signature from the XML document
            signature_hex = signature_tree.find('.//Signature').text
            signature = bytes.fromhex(signature_hex)
            
            # Verify the signature
            hash_obj = SHA256.new(file_content)
            verifier = pkcs1_15.new(public_key)
            try:
                verifier.verify(hash_obj, signature)
                return True
            except (ValueError, TypeError):
                messagebox.showinfo("Error", "Signature is invalid")
                return False
            
        except Exception as e:
            print(f"Verification error: {e}")
            return False
            
    def _clear_variables(self):
        """Clears all input variables and resets the frame to its initial state."""
        self.filename.set("")
        self.keyname.set("")
        self.signaturename.set("")
        self.file_path = None
        self.key_path = None
        self.signature_path = None
