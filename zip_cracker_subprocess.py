import sys
import subprocess
from colorama import init, Fore
from threading import Thread
init()
GREEN = Fore.GREEN
RESET = Fore.RESET
RED = Fore.RED
zip_file = sys.argv[1]
wordlist = sys.argv[2]
n_words = len(list(open(wordlist, "r", encoding="utf-8")))
try_pass = 0
found = False

def unarchive(passwords, file):
    global n_words
    global try_pass
    global found
    while not found:
        try:
            password = next(passwords).strip()
            n_words -= 1
            try_pass += 1
            print(f"{n_words} {try_pass}")
        except StopIteration:
            return

        try:
            subprocess.run(f"7z t -bd -y -P'{password}' {file}",
                shell = True,
                executable="/bin/bash",
                stderr = subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                check=True)
        except Exception as e:
            #print(f"{RED} {e} {RESET}")
            continue
        else:
            print(f"{GREEN} [+] Password found: {password} {RESET}")
            found = True
            return

with open(wordlist, "r", encoding="utf-8") as wordlist:
    workers = []
    for index in range(1, 201):
        workers.append(Thread(target=unarchive, args=(wordlist, zip_file)))

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()

if not found:
    print(f"{RED} [!] Password not found, try other wordlist. {RESET}")
