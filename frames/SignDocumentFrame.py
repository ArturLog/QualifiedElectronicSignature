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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.key_path = None
        self.file_path = None
        self.pinname = tk.StringVar()
        self.filename = tk.StringVar()
        self.keyname = tk.StringVar()
        tk.Label(self, text="Sign document").pack(pady=10)
        
        tk.Button(self, text="Select file", command=self._select_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.filename).pack()
        
        tk.Button(self, text="Find device", command=self._find_device).pack(fill=tk.X, padx=50, pady=5)
        tk.Label(self, textvariable=self.keyname).pack()
        
        tk.Label(self, textvariable="Enter the PIN").pack()
        self.pin_entry = tk.Entry(self, textvariable=self.pinname, show="*", width=4)
        self.pin_entry.pack(pady=5)
        
        tk.Button(self, text="Sign", command=self._sign_controller).pack(fill=tk.X, padx=50, pady=5)
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
    
    def _sign_controller(self):
        if self.key_path and self.file_path and self.controller.check_pin(self.pin_entry.get()):
            if self._sign():
                messagebox.showinfo("Info", "File signed successfully")
                self._clear_variables()
            else:
                messagebox.showerror("Error", "File signing failed")
        else:
            messagebox.showerror("Error", "Select file and put pendrive with private key first")    
    
    def _sign(self):
        try:
            with open(self.file_path, "rb") as f:
                file_content = f.read()
            private_key = self.controller.decrypt_private_key(self.pin_entry.get(), self.key_path)
            
            file_size = os.path.getsize(self.file_path)
            file_extension = os.path.splitext(self.file_path)[1]
            file_modification_date = datetime.fromtimestamp(os.path.getmtime(self.file_path)).isoformat()
            
            hash_obj = SHA256.new(file_content)
            
            signer = pkcs1_15.new(private_key)
            signature = signer.sign(hash_obj)
            
            root = etree.Element('XAdES_Signature')
            file_info = etree.SubElement(root, 'DocumentInfo')
            etree.SubElement(file_info, 'Size').text = str(file_size)
            etree.SubElement(file_info, 'Extension').text = file_extension
            etree.SubElement(file_info, 'ModificationDate').text = file_modification_date
            
            user_info = etree.SubElement(file_info, "UserInfo")
            etree.SubElement(user_info, "SigningUserName").text = str(os.getlogin())
            etree.SubElement(user_info, "SigningUserMAC").text = str(hex(get_mac()))
            
            etree.SubElement(root, 'Signature').text = signature.hex()
            etree.SubElement(root, 'Timestamp').text = datetime.now().isoformat()
            
            xml_string = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode('utf-8')
            
            output_file_path = self.file_path + '.xml'
            with open(output_file_path, 'w') as f:
                f.write(xml_string)
            return True
        except Exception as e:
            print(e)
            return False
    
    def _clear_variables(self):
        self.filename.set("")
        self.keyname.set("")
        self.pinname.set("")
        self.file_path = None
        self.key_path = None  