import tkinter as tk

class AboutUsFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="About us").pack(pady=10)
        description = "This is an application that allows you to:\n" \
                        " sign, verify, encrypt and decrypt documents\n" \
                        "using a qualified electronic signature.\n" \
                        "Authors: \n" \
                        "Artur Śpiewak - 188663\n" \
                        "Przemysław Szumczyk - 188956\n"
        tk.Label(self, text=description).pack(pady=10)
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack()
        
