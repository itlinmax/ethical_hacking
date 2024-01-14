import zipfile, sys
from tqdm import tqdm
from colorama import init, Fore
init()

GREEN = Fore.GREEN
RESET = Fore.RESET
RED = Fore.RED
zip_file = sys.argv[1]
wordlist = sys.argv[2]
zip_file = zipfile.ZipFile(zip_file)
n_words = len(list(open(wordlist, "rb")))
print("Total passwords to test:", n_words)

with open(wordlist, "rb") as wordlist:
    for word in tqdm(wordlist, total=n_words, unit="word"):
        try:
            zip_file.extractall(pwd=word.strip())
        except Exception as e:
            print(f"{RED} {e} {RESET}")
            continue
        else:
            print(f"{GREEN} [+] Password found: {word.decode().strip()} {RESET}")
            exit(0)
print(f"{RED} [!] Password not found, try other wordlist. {RESET}")
