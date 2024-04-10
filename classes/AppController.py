import tkinter as tk
from tkinter import messagebox

DEFAULT_WINDOW_WIDTH = 300
DEFAULT_WINDOW_HEIGHT = 200

class AppController:
    def __init__(self):
        self.window_width = DEFAULT_WINDOW_WIDTH
        self.window_height = DEFAULT_WINDOW_HEIGHT
        
    def main_menu(self):
        
    def sign_document():
        # Placeholder for your sign document functionality
        messagebox.showinfo("Sign Document", "Sign Document functionality goes here.")

    def verify_signature():
        # Placeholder for your verify signature functionality
        messagebox.showinfo("Verify Signature", "Verify Signature functionality goes here.")

    def encrypt_file():
        # Placeholder for your encrypt file functionality
        messagebox.showinfo("Encrypt File", "Encrypt File functionality goes here.")

    def decrypt_file():
        # Placeholder for your decrypt file functionality
        messagebox.showinfo("Decrypt File", "Decrypt File functionality goes here.")

    def about_us():
        # Placeholder for your about us information
        messagebox.showinfo("About Us", "About Us information goes here.")

    # Creating the main window
    root = tk.Tk()
    root.title("Security Application")

    # Configuring the main window's size
    root.geometry("300x200")

    # Creating buttons
    btn_sign_document = tk.Button(root, text="Sign Document", command=sign_document)
    btn_verify_signature = tk.Button(root, text="Verify Signature", command=verify_signature)
    btn_encrypt_file = tk.Button(root, text="Encrypt File", command=encrypt_file)
    btn_decrypt_file = tk.Button(root, text="Decrypt File", command=decrypt_file)
    btn_about_us = tk.Button(root, text="About Us", command=about_us)

    # Positioning buttons
    btn_sign_document.pack(fill=tk.X, padx=50, pady=5)
    btn_verify_signature.pack(fill=tk.X, padx=50, pady=5)
    btn_encrypt_file.pack(fill=tk.X, padx=50, pady=5)
    btn_decrypt_file.pack(fill=tk.X, padx=50, pady=5)
    btn_about_us.pack(fill=tk.X, padx=50, pady=5)

    # Running the application
    root.mainloop()
