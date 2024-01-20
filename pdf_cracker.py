import pikepdf, sys
from tqdm import tqdm

pdf_file = sys.argv[1]
wordlist = sys.argv[2]

n_words = len(list(open(wordlist, "r", encoding="utf-8")))
print(n_words)

with open(wordlist, "r", encoding="utf-8") as wordlist:
    for password in tqdm(iterable=wordlist, desc="Decrypting PDF", total=n_words, unit="password"):
        try:
            with pikepdf.open(pdf_file, password=password.strip()) as pdf:
                print("[+] Password found:", password)
                break
        #except pikepdf._qpdf.PasswordError as e:
        except pikepdf._core.PasswordError as e:
            continue
