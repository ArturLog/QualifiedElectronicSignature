import tkinter as tk

class SignDocumentFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Sign Document Page").pack(pady=10)
        tk.Button(self, text="Back to Main Page", command=lambda: controller.show_frame("MainPage")).pack()
