import tkinter as tk
from tkinter import messagebox

class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Button(self, text="Sign Document", command=lambda: controller.show_frame("SignDocumentFrame")).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Verify Signature", command=self.verify_signature).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Encrypt File", command=self.encrypt_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Decrypt File", command=self.decrypt_file).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="About Us", command=self.about_us).pack(fill=tk.X, padx=50, pady=5)

    def sign_document(self):
        messagebox.showinfo("Sign Document", "Sign Document functionality goes here.")

    def verify_signature(self):
        messagebox.showinfo("Verify Signature", "Verify Signature functionality goes here.")

    def encrypt_file(self):
        messagebox.showinfo("Encrypt File", "Encrypt File functionality goes here.")

    def decrypt_file(self):
        messagebox.showinfo("Decrypt File", "Decrypt File functionality goes here.")

    def about_us(self):
        messagebox.showinfo("About Us", "About Us information goes here.")