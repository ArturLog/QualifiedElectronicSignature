from classes.RSAKeysGenerator import RSAKeysGenerator

if __name__ == "__main__":
    print("Type your PIN to generate a new RSA key pair")
    pin = input("Enter your PIN: ")
    rsa_keys_generator = RSAKeysGenerator(pin)
    rsa_keys_generator.generate_rsa_keys()
    rsa_keys_generator.save_keys()