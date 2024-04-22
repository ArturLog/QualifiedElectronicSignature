import os
import psutil
import hashlib
import tkinter as tk
from tkinter import messagebox, filedialog
from frames.MainFrame import MainFrame
from frames.SignDocumentFrame import SignDocumentFrame
from frames.VerifySignatureFrame import VerifySignatureFrame
from frames.EncryptFrame import EncryptFrame
from frames.DecryptFrame import DecryptFrame
from frames.AboutUsFrame import AboutUsFrame
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from config import *

class AppController(tk.Tk):
    """
    Main application controller that manages the GUI using tkinter and handles all operations.

    Attributes:
        frames (dict): A dictionary to store the different frames of the application.
    """

    def __init__(self):
        """
        Initialize the application controller, setting the window title, geometry, and frames.
        """
        super().__init__()
        self.title(DEFAULT_TITLE)
        self.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")

        # Container setup for placing all frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initialize and place all frames within the container
        self.frames = {}
        for FrameClass in (MainFrame, SignDocumentFrame, VerifySignatureFrame, EncryptFrame, DecryptFrame, AboutUsFrame):
            frame = FrameClass(parent=container, controller=self)
            frame_name = FrameClass.__name__
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainFrame")

    def select_file(self, extensions=["txt"]):
        """
        Open a file dialog to select a file with specific extensions.

        Args:
            extensions (list): A list of acceptable file extensions.

        Returns:
            str: The path of the selected file if successful, otherwise an empty string.
        """
        file_path = filedialog.askopenfilename()
        if file_path and self.check_extension(file_path, extensions):
            return file_path
        return ""

    def show_frame(self, frame_name):
        """
        Display the frame with the given name.

        Args:
            frame_name (str): The name of the frame to display.
        """
        frame = self.frames[frame_name]
        frame.tkraise()

    def check_extension(self, file_path, extensions):
        """
        Check if the file has a valid extension.

        Args:
            file_path (str): Path of the file to check.
            extensions (list): List of valid extensions.

        Returns:
            bool: True if file extension is valid, otherwise False.
        """
        if file_path.split('.')[-1] not in extensions:
            messagebox.showerror("Error", "Invalid file extension")
            return False
        return True

    def check_external_storage(self):
        """
        Check for the presence of any external storage device.

        Returns:
            str: The mount point of the first removable storage found, or None if no such storage exists.
        """
        partitions = psutil.disk_partitions(all=True)
        for partition in partitions:
            if 'removable' in partition.opts:
                if os.path.exists(partition.mountpoint):
                    return partition.mountpoint
        return None

    def check_private_key_on_external_storage(self, mountpoint):
        """
        Search for a PEM private key file in the specified mount point.

        Args:
            mountpoint (str): The mountpoint to search in.

        Returns:
            str: Path to the PEM file if found, otherwise None.
        """
        files = os.listdir(mountpoint)
        for file in files:
            if file.endswith(".pem"):
                return os.path.join(mountpoint, file)
        return None

    def decrypt_private_key(self, pin, key_path):
        """
        Decrypt a private key using a PIN.

        Args:
            pin (str): The PIN to use for decryption.
            key_path (str): The path to the encrypted key file.

        Returns:
            RSA key object if decryption is successful, otherwise None.
        """
        with open(key_path, "rb") as file:
            encrypted_key = file.read()

        # Extract initialization vector and encrypted key part
        iv = encrypted_key[:AES.block_size]
        encrypted_key = encrypted_key[AES.block_size:]

        # Generate decryption key from PIN
        key = hashlib.sha256(pin.encode()).digest()
        cipher = AES.new(key, AES.MODE_CFB, iv)
        decrypted_key = cipher.decrypt(encrypted_key)

        try:
            return RSA.import_key(decrypted_key)
        except Exception as e:
            print(f"Failed to decrypt key: {e}")
            return None

    def check_pin(self, pin):
        """
        Validate the PIN entered by the user.

        Args:
            pin (str): The PIN to validate.

        Returns:
            bool: True if the PIN is valid, otherwise False.
        """
        if not pin:
            messagebox.showerror("Error", "Type PIN first")
            return False
        elif len(pin) != PIN_LENGTH or not pin.isdigit():
            messagebox.showerror("Error", f"PIN must be exactly {PIN_LENGTH} digits")
            return False
        return True
