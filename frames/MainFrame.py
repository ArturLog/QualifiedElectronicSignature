import tkinter as tk

class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self._create_label()
        self._create_buttons()
        
    def _create_label(self):
        tk.Label(self, text="Welcome! What do you want to do today?").pack(pady=10)   
        
    def _create_buttons(self):
        tk.Button(self, text="Sign Document", command=lambda: self.controller.show_frame("SignDocumentFrame")).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Verify Signature", command=lambda: self.controller.show_frame("VerifySignatureFrame")).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Encrypt File", command=lambda: self.controller.show_frame("EncryptFrame")).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Decrypt File", command=lambda: self.controller.show_frame("DecryptFrame")).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="About Us", command=lambda: self.controller.show_frame("AboutUsFrame")).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Exit", command=self.exit).pack(fill=tk.X, padx=50, pady=5)
        
    def exit(self):
        self.controller.quit()
        self.controller.destroy()