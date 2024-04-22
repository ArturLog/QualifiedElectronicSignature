# Configuration file for setting application-wide constants.

# Default dimensions for the application window.
DEFAULT_WINDOW_WIDTH = 400
DEFAULT_WINDOW_HEIGHT = 360

# Default title for the application window.
DEFAULT_TITLE = "Security Application - Artur Śpiewak & Przemysław Szumczyk"

# Acceptable file extensions for keys (used in file dialogs).
KEY_EXTENSION = ["pem"]

# Acceptable file extensions for documents that can be signed, encrypted, or decrypted.
FILE_EXTENSION = ["txt", "pdf"]

# Acceptable file extension for signature files.
SIGNATURE_EXTENSION = ["xml"]

# Required length of the PIN for encryption and decryption operations.
PIN_LENGTH = 4

# Use a 4096-bit RSA key
DEFAULT_RSA_KEY_SIZE = 4096  

# AES key length set to 32 bytes (256 bits) for AES-256 encryption
DEFAULT_AES_KEY_LENGTH = 32  