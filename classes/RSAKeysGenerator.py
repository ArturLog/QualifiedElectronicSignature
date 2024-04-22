import hashlib
from Crypto.PublicKey import RSA 
from Crypto.Cipher import AES

# Default constants for key sizes
DEFAULT_RSA_KEY_SIZE = 4096  # Use a 4096-bit RSA key
DEFAULT_AES_KEY_LENGTH = 32  # AES key length set to 32 bytes (256 bits) for AES-256 encryption

class RSAKeysGenerator:
    """
    Handles the generation, encryption, and storage of RSA keys. The private key is encrypted
    using AES-256 with a key derived from a provided PIN.
    """
    
    def __init__(self, pin):
        """
        Initialize the RSAKeysGenerator with a PIN used to encrypt the private key.

        Args:
            pin (str): PIN used to derive the AES key for encrypting the private key.
        """
        self._private_key = None
        self._public_key = None
        self._pin = pin
    
    def generate_keys(self):
        """
        Generates an RSA key pair of specified size.
        """
        self._private_key = RSA.generate(bits=DEFAULT_RSA_KEY_SIZE)
        self._public_key = self._private_key.publickey()
        print("Generated RSA key pair successfully!")

    def _encrypt_private_key(self):
        """
        Encrypts the private key using AES-256 encryption derived from the provided PIN.

        Returns:
            bytes: The concatenated initialization vector (IV) and the encrypted private key.
        """
        key = hashlib.sha256(self._pin.encode()).digest()  # Derive the AES key from the provided PIN
        cipher = AES.new(key, AES.MODE_CFB)  # AES in CFB mode, IV is generated automatically
        
        private_key_bytes = self._private_key.export_key()  # Export private key to bytes
        encrypted_private_key = cipher.encrypt(private_key_bytes)  # Encrypt the private key bytes
        
        print("Encrypted private key successfully!")
        return cipher.iv + encrypted_private_key  # Return IV and encrypted private key as a single byte sequence

    def save_keys(self):
        """
        Saves the RSA public key and the encrypted private key to files in PEM format.
        """
        # Save the public key in PEM format
        with open("./keys/public_key.pem", "wb") as f:
            f.write(self._public_key.export_key())
        print("Saved public key successfully!")
        
        # Save the encrypted private key, including the IV, for secure storage
        with open("./keys/private_key.pem", "wb") as f:
            f.write(self._encrypt_private_key())
        print("Saved private key successfully!")
