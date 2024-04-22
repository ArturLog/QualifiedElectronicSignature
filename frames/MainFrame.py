import tkinter as tk

class MainFrame(tk.Frame):
    """
    The main interface frame of the application, presenting options to the user for various operations
    such as signing, verifying, encrypting, and decrypting documents, as well as accessing application information.
    """
    
    def __init__(self, parent, controller):
        """
        Initialize the MainFrame within the parent container.

        Args:
            parent (tk.Widget): The parent widget in which this frame will be placed.
            controller (object): The main application controller which manages navigation between frames.
        """
        super().__init__(parent)
        self.controller = controller
        
        self._create_label()  # Initialize the main label of the frame
        self._create_buttons()  # Initialize the action buttons of the frame
    
    def _create_label(self):
        """Create and pack the welcome label to the frame."""
        tk.Label(self, text="Welcome! What do you want to do today?").pack(pady=10)   
        
    def _create_buttons(self):
        """
        Create and pack buttons that allow the user to navigate to different functionalities
        of the application or exit the application.
        """
        actions = [
            ("Sign Document", "SignDocumentFrame"),
            ("Verify Signature", "VerifySignatureFrame"),
            ("Encrypt File", "EncryptFrame"),
            ("Decrypt File", "DecryptFrame"),
            ("About Us", "AboutUsFrame"),
            ("Exit", self.exit)
        ]
        for text, command in actions:
            tk.Button(self, text=text, command=lambda c=command: self.controller.show_frame(c) if isinstance(c, str) else c()).pack(fill=tk.X, padx=50, pady=5)
        
    def exit(self):
        """Terminate the application."""
        self.controller.quit()  # Stop the tkinter main loop
        self.controller.destroy()  # Destroy all widgets
