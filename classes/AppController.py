import tkinter as tk
from tkinter import messagebox
from frames.MainFrame import MainFrame
from frames.SignDocumentFrame import SignDocumentFrame
from frames.VerifySignatureFrame import VerifySignatureFrame
from frames.EncryptFrame import EncryptFrame
from frames.DecryptFrame import DecryptFrame
from frames.AboutUsFrame import AboutUsFrame


DEFAULT_WINDOW_WIDTH = 400
DEFAULT_WINDOW_HEIGHT = 300
DEFAULT_TITLE = "Security Application - Artur Śpiewak & Przemysław Szumczyk"

class AppController(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title(DEFAULT_TITLE)
        self.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
        
        self.frames = {}
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initializing all frames
        for F in (MainFrame, SignDocumentFrame, VerifySignatureFrame, EncryptFrame, DecryptFrame, AboutUsFrame):
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainFrame")

    def show_frame(self, frame_name):
        '''Show a frame for the given frame name'''
        frame = self.frames[frame_name]
        frame.tkraise()
    
    def check_extension(self, file_path ,extensions):
        if file_path.split('.')[-1] not in extensions:
            messagebox.showerror("Error", "Invalid file extension")
            return False
        return True