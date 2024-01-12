import pathlib, os, secrets, base64, getpass
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def generate_salt(size=16):
    """Generate the salt used for key derivation,
    `size` is the length of the salt to generate"""
    return secrets.token_bytes(size)

def derive_key(salt, password):
    """Derive the key from the `password` using the passed
    `salt`"""
    kdf = Scrypt(salt=salt, length=32 , n=2**14, r=8 ,p=1)
    return kdf.derive(password.encode())

def load_salt():
    # load salt from salt.salt file
    return open("salt.salt", "rb").read()

def ask_overwrite_exist_salt_file():
    """Check whether the salt.salt file exists
    and warn the user about the danger of
    overwriting an existing salt.salt file"""
    if os.path.isfile("salt.salt"):
        print("Attention! With the '-s' option you will overwrite an existing salt file.\n",
              "If you do not want to overwrite the file, enter 'no'")
        user_input = input("Do you want to overwrite existing salt file? (yes/no): ")
        if user_input.lower() in ["yes", "y"]:
            return True
        else:
            #print("Exiting script...")
            print("I will use existing file to salt password :)")
            return False
    return True

def generate_key(password, salt_size=16 , load_existing_salt=False, save_salt=True):
    """Generates a key from a `password` and the salt.
    If `load_existing_salt` is True, it'll load the salt from a file
    in the current directory called "salt.salt".
    If `save_salt` is True, then it will generate a new salt
    and save it to "salt.salt"""

    if load_existing_salt:
        salt = load_salt()
    elif save_salt:
        # generate new salt and save it
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)
    derived_key = derive_key(salt, password)
    return base64.urlsafe_b64encode(derived_key)

def encrypt(filename, key):
    """Given a filename (str) and key (bytes), it encrypts the file
    and write it"""
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def decrypt(filename, key):
    """Given a filename (str) and key (bytes), it decrypts the file
    and write it"""
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
        try:
            decrypted_data = f.decrypt(encrypted_data)
        except cryptography.fernet.InvalidToken:
            print("[!] Invalid token, most likely the password is incorrect")
            return
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def encrypt_folder(foldername, key):
    # if it's a folder, encrypt the entire folder (i.e all the containing files)
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[*] Encrypting {child}")
            encrypt(child, key)
        elif child.is_dir():
            encrypt_folder(child, key)

def decrypt_folder(foldername, key):
    # if it's a folder, decrypt the entire folder
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[*] Decrypting {child}")
            decrypt(child, key)
        elif child.is_dir():
            decrypt_folder(child, key)

def check_passwords_equality(passwd1, passwd2):
    """make sure the user has entered the same password"""
    if passwd1 == passwd2:
        return True
    return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="File Encryptor Script with a Password")
    parser.add_argument("path", help="Path to encrypt/decrypt, can be a file or an entire folder")
    parser.add_argument("-s", "--salt-size", help="If this is set, a new salt with the passed size is generated", type=int)
    parser.add_argument("-e", "--encrypt", action="store_true", help="Whether to encrypt the file/folder, only -e or -d can be specified.")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Whether to decrypt the file/folder, only -e or -d can be specified.")
    args = parser.parse_args()

    if args.encrypt:
        password1 = getpass.getpass("Enter the password for encryption: ")
        password2 = getpass.getpass("Enter the same password for second time: ")
        if not check_passwords_equality(password1, password2):
            print("The entered passwords are not the same")
            exit(1)
        password = password1
    elif args.decrypt:
        password = getpass.getpass("Enter the password you used for encryption: ")

    if args.salt_size:
        if ask_overwrite_exist_salt_file():
            key = generate_key(password, salt_size=args.salt_size, save_salt=True)
        else:
            key = generate_key(password, load_existing_salt=True)
    else:
        key = generate_key(password, load_existing_salt=True)
    encrypt_ = args.encrypt
    decrypt_ = args.decrypt

    if encrypt_ and decrypt_:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")
    elif encrypt_:
        if os.path.isfile(args.path):
            encrypt(args.path, key)
        elif os.path.isdir(args.path):
            encrypt_folder(args.path, key)
    elif decrypt_:
        if os.path.isfile(args.path):
            decrypt(args.path, key)
        elif os.path.isdir(args.path):
            decrypt_folder(args.path, key)
    else:
        raise TypeError("Please specify whether you want to encrypt the file/folder or decrypt it.")
