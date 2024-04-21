import tkinter as tk
from lxml import etree
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from tkinter import messagebox
from config import KEY_EXTENSION, FILE_EXTENSION, SIGNATURE_EXTENSION

class VerifySignatureFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.signature_path = None
        self.file_path = None
        self.key_path = None 
        self.filename = tk.StringVar()
        self.keyname = tk.StringVar()
        self.signaturename = tk.StringVar()
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
        self.file_path = self.controller.select_file(extensions=FILE_EXTENSION)
        self.filename.set("File:\n" + self.file_path)
        
    def _select_key(self):
        self.key_path = self.controller.select_file(extensions=KEY_EXTENSION)
        self.keyname.set("Key:\n" + self.key_path)
        
    def _select_signature(self):
        self.signature_path = self.controller.select_file(extensions=SIGNATURE_EXTENSION)
        self.signaturename.set("Signature:\n" + self.signature_path)
    
    def _verify_controller(self):
        if self.key_path and self.file_path and self.signature_path:
            if self._verify():
                messagebox.showinfo("Info", "File verified successfully")
                self._clear_variables()
            else:
                messagebox.showerror("Error", "File verification failed")
        else:
            messagebox.showerror("Error", "Select file, key and signature first")         
    
    def _verify(self):
        try:
            with open(self.file_path, "rb") as f:
                file_content = f.read()
            with open(self.key_path, "r") as key:
                public_key = RSA.import_key(key.read())
            with open(self.signature_path, 'rb') as f:
                signature_tree = etree.parse(f)
                
            hash_obj = SHA256.new(file_content)    
            
            signature_hex = signature_tree.find('.//Signature').text
            signature = bytes.fromhex(signature_hex)
            
            verifier = pkcs1_15.new(public_key)
            try:
                verifier.verify(hash_obj, signature)
                return True
            except (ValueError, TypeError):
                messagebox.showinfo("Error", "Signature is invalid") 
                return False
            
        except Exception as e:
            print(e)
            return False  
            
    def _clear_variables(self):
        self.filename.set("")
        self.keyname.set("")
        self.signaturename.set("")
        self.signature_path = None
        self.file_path = None
        self.key_path = None     