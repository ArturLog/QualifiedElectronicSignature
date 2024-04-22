import tkinter as tk

class AboutUsFrame(tk.Frame):
    """
    A frame that provides information about the application and its authors.
    This frame is part of a larger application that handles electronic document operations.
    """
    def __init__(self, parent, controller):
        """
        Initialize the About Us frame within the parent container.

        Args:
            parent (tk.Widget): The parent widget in which this frame will be placed.
            controller (object): The main application controller which manages navigation between frames.
        """
        super().__init__(parent)  # Initialize the superclass (tk.Frame)
        self.controller = controller  # Reference to the main application controller

        # Title label for the 'About Us' frame
        tk.Label(self, text="About us").pack(pady=10)

        # Multiline description of the application and its authors
        description = (
            "This is an application that allows you to:\n"
            " sign, verify, encrypt, and decrypt documents\n"
            "using a qualified electronic signature.\n"
            "Authors: \n"
            "Artur Śpiewak - 188663\n"
            "Przemysław Szumczyk - 188956\n"
        )
        tk.Label(self, text=description).pack(pady=10)  # Display the description

        # Button to return to the main menu, uses a lambda to delay execution of the command
        tk.Button(self, text="Main menu", command=lambda: controller.show_frame("MainFrame")).pack()
