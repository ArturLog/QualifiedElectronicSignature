from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from Crypto.PublicKey import RSA 
from Crypto.Cipher import AES 
from Crypto.Protocol.KDF import PBKDF2 
from Crypto.Random import get_random_bytes
import os

DEFAULT_RSA_KEY_SIZE = 4096 # Project requirement: 4096-bit key size
DEFAULT_RSA_PUBLIC_EXPONENT = 65537 # Commonly used public exponent for RSA
DEFAULT_AES_KEY_LENGTH = 32 # AES key length for AES-256 encryption
DEFAULT_AES_ITERATIONS = 100000 # Number of iterations for the key derivation function
DEFAULT_AES_SALT_LENGTH = 16 # Salt length for the key derivation function
DEFAULT_AES_IV_LENGTH = 16 # AES initialization vector length

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
    
    def generate_keys2(self):
        """
        Generates a pair of RSA keys with a 4096-bit key size and a public exponent of 65537,
        which are standard and secure values for RSA encryption.
        """
        self._private_key = rsa.generate_private_key(
            public_exponent=DEFAULT_RSA_PUBLIC_EXPONENT,  
            key_size=DEFAULT_RSA_KEY_SIZE,  
            backend=default_backend()   # Use the default backend
        )
        self._public_key = self._private_key.public_key()
        print("Generated RSA key pair successfully!")

    def _encrypt_private_key(self):
        key = PBKDF2(self._pin, dkLen=DEFAULT_AES_KEY_LENGTH)  # Derive the AES key
        
        cipher = AES.new(key, AES.MODE_CFB)  # Create a new cipher object, automatically generates IV
        
        private_key_bytes = self._private_key.export_key()  # Export the private key
        encrypted_private_key = cipher.encrypt(private_key_bytes)  # Encrypt the private key
        
        print("Encrypted private key successfully!")
        return cipher.iv + encrypted_private_key  # Return the salt, IV, and encrypted private key as a single byte string

    def _encrypt_private_key2(self):
        """
        Encrypts the private key using AES in CFB mode with a key derived from the provided PIN.
        This method uses a salt for the key derivation function to enhance security.
        
        :return: The concatenated salt, initialization vector (IV), and the encrypted private key.
        """
        salt = os.urandom(DEFAULT_AES_SALT_LENGTH)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),  # Secure hashing algorithm
            length=DEFAULT_AES_KEY_LENGTH,  
            salt=salt,
            iterations=DEFAULT_AES_ITERATIONS,
            backend=default_backend()   # Use the default backend
        )
        aes_key = kdf.derive(self._pin.encode()) # Derive a secure AES key from the PIN

        iv = os.urandom(DEFAULT_AES_IV_LENGTH)
        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_private_key = encryptor.update(self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )) + encryptor.finalize()
        print("Encrypted private key successfully!")
        return salt + iv + encrypted_private_key    # Return the encrypted data (salt + IV + ciphertext)

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
            