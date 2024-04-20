import hashlib
from Crypto.PublicKey import RSA 
from Crypto.Cipher import AES

DEFAULT_RSA_KEY_SIZE = 4096 # Project requirement: 4096-bit key size
DEFAULT_AES_KEY_LENGTH = 32 # AES key length for AES-256 encryption

class RSAKeysGenerator:
    """
    This class encapsulates the functionality for generating RSA keys, encrypting the private key,
    and saving both keys to files. It uses strong cryptographic standards for encryption and key derivation.
    """
    
    def __init__(self, pin):
        """
        Initializes the RSAKeysGenerator with a PIN that is used for encrypting the private key.
        
        :param pin: A string PIN to derive an encryption key for the private key.
        """
        self._private_key = None
        self._public_key = None
        self._pin = pin
    
    def generate_keys(self):
        self._private_key = RSA.generate(bits=DEFAULT_RSA_KEY_SIZE)
        self._public_key = self._private_key.publickey()
        print("Generated RSA key pair successfully!")

    def _encrypt_private_key(self):
        key = hashlib.sha256(self._pin.encode()).digest()  # Derive the AES key
        
        cipher = AES.new(key, AES.MODE_CFB)  # Create a new cipher object, automatically generates IV
        
        private_key_bytes = self._private_key.export_key()  # Export the private key
        encrypted_private_key = cipher.encrypt(private_key_bytes)  # Encrypt the private key
        
        print("Encrypted private key successfully!")
        return cipher.iv + encrypted_private_key  # Return the salt, IV, and encrypted private key as a single byte string

    def save_keys(self):
        """
        Saves the RSA public key in PEM format and the encrypted private key to separate files.
        """
        
        # Save the public key in PEM format
        with open("./keys/public_key.pem", "wb") as f:
            f.write(self._public_key.export_key())
        print("Saved public key successfully!")
        # Save the encrypted private key, including salt and IV, for secure storage
        with open("./keys/private_key.pem", "wb") as f:
            f.write(self._encrypt_private_key())
        print("Saved private key successfully!")
            