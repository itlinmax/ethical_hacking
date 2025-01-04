import subprocess
import getpass
import os
import sys
import argparse
import pathlib
"""
gpg (GnuPG) 2.2.27
libgcrypt 1.9.4
Copyright (C) 2021 Free Software Foundation, Inc.
License GNU GPL-3.0-or-later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Supported algorithms:
Pubkey: RSA, ELG, DSA, ECDH, ECDSA, EDDSA
Cipher: IDEA, 3DES, CAST5, BLOWFISH, AES, AES192, AES256, TWOFISH,
        CAMELLIA128, CAMELLIA192, CAMELLIA256
Hash: SHA1, RIPEMD160, SHA256, SHA384, SHA512, SHA224
Compression: Uncompressed, ZIP, ZLIB, BZIP2
"""


def encrypt_file(file, password, shred=False):
    print(f"[*] Encrypting {file}")
    try:
        gpg_process = subprocess.run([f"gpg --yes --batch --symmetric --cipher-algo AES256 --armor --passphrase {password} -o '{file}.asc' '{file}'"], check=True, shell=True, executable="/bin/bash", capture_output=True, encoding="utf-8")
    except subprocess.CalledProcessError as exc:
        print(f"Process gpg failed because did not return a successful return code: [{exc.returncode}]")
        print(f"[{exc.stderr}]")
        sys.exit(1)
    if gpg_process.returncode == 0:
        try:
            if shred:
                print(f"[*] Shreding original {file}")
                subprocess.run([f"shred -zu -n5 '{file}'"], check=True, shell=True, executable="/bin/bash", capture_output=True, encoding="utf-8")
            else:
                print(f"[*] Removing original {file}")
                subprocess.run([f"rm -rf '{file}'"], check=True, shell=True, executable="/bin/bash", capture_output=True, encoding="utf-8")
        except subprocess.CalledProcessError as exc:
            print(f"Process shred failed because did not return a successful return code: [{exc.returncode}]")
            print(f"[{exc.stderr}]")

def encrypt_folder(foldername, password, shred):
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            encrypt_file(child, password, shred)
        elif child.is_dir():
            encrypt_folder(child, password, shred)


def decrypt_file(file, password):
    if str(file).endswith(".asc"):
        print(f"[*] Decrypting {file}")
        encripted_name = os.path.splitext(file)[0]
        try:
            completed_process = subprocess.run([f"gpg --yes --batch --decrypt --cipher-algo AES256 --passphrase {password} -o '{encripted_name}' '{file}' && rm '{file}'"], check=True, shell=True, executable="/bin/bash", capture_output=True, encoding="utf-8")
        except subprocess.CalledProcessError as exc:
            print(f"Process gpg failed because did not return a successful return code: [{exc.returncode}]")
            print(f"[{exc.stderr}]")

def decrypt_folder(foldername, password):
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            decrypt_file(child, password)
        elif child.is_dir():
            decrypt_folder(child, password)


def check_passwords_equality(passwd1, passwd2):
    """make sure the user has entered the same password"""
    if passwd1 == passwd2:
        return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Encryptor Script with a Password")
    parser.add_argument("path", help="Path to encrypt/decrypt, can be a file or an entire folder")
    parser.add_argument("-e", "--encrypt", action="store_true", help="Whether to encrypt the file/folder, only -e or -d can be specified.")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Whether to decrypt the file/folder, only -e or -d can be specified.")
    parser.add_argument("-p", "--password", help="The password you want to encrypt/decrypt files with.")
    parser.add_argument("-s", "--shred", default=False, action="store_true", help="Shred file after encrypting.")
    args = parser.parse_args()
    encrypt_ = args.encrypt
    decrypt_ = args.decrypt
    password = args.password
    shred = args.shred
    if encrypt_ and decrypt_:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")
    elif encrypt_:
        if not password:
            password1 = getpass.getpass("Enter the password for encryption: ")
            password2 = getpass.getpass("Enter the same password for second time: ")
            if not check_passwords_equality(password1, password2):
                print("The entered passwords are not the same")
                sys.exit(1)
            password = password1
        if os.path.isfile(args.path):
            encrypt_file(args.path, password, shred)
        elif os.path.isdir(args.path):
            encrypt_folder(args.path, password, shred)
        else:
            print(f"ERROR: such file or folder does not exist: [{os.path.abspath(args.path)}]")
            sys.exit(1)

    elif decrypt_:
        if not password:
            password = getpass.getpass("Enter the password you used for encryption: ")
        if os.path.isfile(args.path):
            decrypt_file(args.path, password)
        elif os.path.isdir(args.path):
            decrypt_folder(args.path, password)
    else:
        raise TypeError("Please specify whether you want to encrypt the file/folder or decrypt it.")
