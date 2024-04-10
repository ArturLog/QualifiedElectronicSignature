import tkinter as tk

class DecryptFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Decrypt").pack(pady=10)
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack()
        
