import tkinter as tk
import os
from lxml import etree
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from datetime import datetime
from tkinter import messagebox
from config import FILE_EXTENSION
from uuid import getnode as get_mac

class SignDocumentFrame(tk.Frame):
    """
    A frame for signing documents using a private key that is secured on an external device.
    This frame allows the user to select a document, find a private key, enter a PIN for decryption,
    and then sign the document.
    """
    
    def __init__(self, parent, controller):
        """
        Initialize the Sign Document frame within the parent container.

        Args:
            parent (tk.Widget): The parent widget in which this frame will be placed.
            controller (object): The main application controller which manages navigation between frames.
        """
        super().__init__(parent)
        self.controller = controller
        self.key_path = None
        self.file_path = None
        self.pinname = tk.StringVar()
        self.filename = tk.StringVar()
        self.keyname = tk.StringVar()

        # Create UI elements for signing documents
        tk.Label(self, text="Sign document").pack(pady=10)
        tk.Button(self, text="Select file", command=self._select_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.filename).pack()
        tk.Button(self, text="Find device", command=self._find_device).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.keyname).pack()
        tk.Label(self, text="Enter the PIN").pack()
        self.pin_entry = tk.Entry(self, textvariable=self.pinname, show="*", width=4)
        self.pin_entry.pack(pady=5)
        tk.Button(self, text="Sign", command=self._sign_controller).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack(fill=tk.X, padx=50, pady=5)
    
    def _select_file(self):
        """Selects a file for signing and updates the filename variable in the UI."""
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
    
    def _sign_controller(self):
        """
        Controller method that manages the document signing process,
        including validation of inputs and reporting of the signing status.
        """
        if self.key_path and self.file_path and self.controller.check_pin(self.pin_entry.get()):
            if self._sign():
                messagebox.showinfo("Info", "File signed successfully")
                self._clear_variables()
            else:
                messagebox.showerror("Error", "File signing failed")
        else:
            messagebox.showerror("Error", "Select file and put pendrive with private key first")
    
    def _sign(self):
        """
        Performs the document signing using the private key decrypted with the entered PIN.

        Returns:
            bool: True if the signing process is successful, otherwise False.
        """
        try:
            with open(self.file_path, "rb") as file:
                file_content = file.read()
            private_key = self.controller.decrypt_private_key(self.pin_entry.get(), self.key_path)

            # Collect document metadata for the signature
            file_size = os.path.getsize(self.file_path)
            file_extension = os.path.splitext(self.file_path)[1]
            file_mod_date = datetime.fromtimestamp(os.path.getmtime(self.file_path)).isoformat()

            # Create signature
            hash_obj = SHA256.new(file_content)
            signer = pkcs1_15.new(private_key)
            signature = signer.sign(hash_obj)

            # Create XML structure for the signed document
            root = etree.Element('XAdES_Signature')
            doc_info = etree.SubElement(root, 'DocumentInfo')
            etree.SubElement(doc_info, 'Size').text = str(file_size)
            etree.SubElement(doc_info, 'Extension').text = file_extension
            etree.SubElement(doc_info, 'ModificationDate').text = file_mod_date
            user_info = etree.SubElement(root, 'UserInfo')
            etree.SubElement(user_info, 'SigningUserName').text = os.getlogin()
            etree.SubElement(user_info, 'SigningUserMAC').text = hex(get_mac())
            etree.SubElement(root, 'Signature').text = signature.hex()
            etree.SubElement(root, 'Timestamp').text = datetime.now().isoformat()

            # Save the signed document as XML
            xml_string = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode('utf-8')
            output_file_path = self.file_path + '.xml'
            with open(output_file_path, 'w') as file:
                file.write(xml_string)
            return True
        except Exception as e:
            print(f"Signing error: {e}")
            return False
    
    def _clear_variables(self):
        """Clears all input variables and resets the frame to its initial state."""
        self.filename.set("")
        self.keyname.set("")
        self.pinname.set("")
        self.file_path = None
        self.key_path = None  
