import subprocess
import getpass
import os
import sys
import argparse
import pathlib


def encrypt_file(file, password):
    print(f"[*] Encrypting {file}")
    try:
        gpg_process = subprocess.run([f"gpg --yes --batch --symmetric --cipher-algo AES256 --armor --passphrase {password} -o '{file}.asc' '{file}'"], check=True, shell=True, executable="/bin/bash", capture_output=True, encoding="utf-8")
    except subprocess.CalledProcessError as exc:
        print(f"Process gpg failed because did not return a successful return code: [{exc.returncode}]")
        print(f"[{exc.stderr}]")
        sys.exit(1)
    try:
        print(f"[*] Shreding original {file}")
        shred_process = subprocess.run([f"shred -zu -n5 '{file}'"], check=True, shell=True, executable="/bin/bash", capture_output=True, encoding="utf-8")
    except subprocess.CalledProcessError as exc:
        print(f"Process shred failed because did not return a successful return code: [{exc.returncode}]")
        print(f"[{exc.stderr}]")


def decrypt_file(file, password):
    if str(file).endswith(".asc"):
        print(f"[*] Decrypting {file}")
        encripted_name = os.path.splitext(file)[0]
        try:
            completed_process = subprocess.run([f"gpg --yes --batch --decrypt --passphrase {password} -o '{encripted_name}' '{file}' && rm '{file}'"], check=True, shell=True, executable="/bin/bash", capture_output=True, encoding="utf-8")
        except subprocess.CalledProcessError as exc:
            print(f"Process gpg failed because did not return a successful return code: [{exc.returncode}]")
            print(f"[{exc.stderr}]")


def encrypt_folder(foldername, password):
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            encrypt_file(child, password)
        elif child.is_dir():
            encrypt_folder(child, password)


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
    args = parser.parse_args()
    encrypt_ = args.encrypt
    decrypt_ = args.decrypt
    if encrypt_ and decrypt_:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")
    elif encrypt_:
        password1 = getpass.getpass("Enter the password for encryption: ")
        password2 = getpass.getpass("Enter the same password for second time: ")
        if not check_passwords_equality(password1, password2):
            print("The entered passwords are not the same")
            sys.exit(1)
        password = password1
        if os.path.isfile(args.path):
            encrypt_file(args.path, password)
        elif os.path.isdir(args.path):
            encrypt_folder(args.path, password)
    elif decrypt_:
        password = getpass.getpass("Enter the password you used for encryption: ")
        if os.path.isfile(args.path):
            decrypt_file(args.path, password)
        elif os.path.isdir(args.path):
            decrypt_folder(args.path, password)
    else:
        raise TypeError("Please specify whether you want to encrypt the file/folder or decrypt it.")
