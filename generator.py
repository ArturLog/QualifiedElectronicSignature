from classes.RSAKeysGenerator import RSAKeysGenerator

if __name__ == "__main__":
    # Prompt the user to enter a PIN used for encrypting the RSA private key.
    print("Type your PIN to generate a new RSA key pair")
    pin = input("Enter your PIN: ")

    # Create an instance of the RSAKeysGenerator with the provided PIN.
    rsa_keys_generator = RSAKeysGenerator(pin)

    # Generate the RSA key pair.
    rsa_keys_generator.generate_keys()

    # Save the generated keys to files.
    rsa_keys_generator.save_keys()

    # Prompt the user to press Enter to exit the program after the keys are saved.
    input("Generator end job. Press Enter to exit.")
