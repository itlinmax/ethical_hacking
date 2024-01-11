import requests
import threading
from threading import Thread, Lock
from queue import Queue
from threading import active_count

domain = "google.com"
in_queue = Queue()
out_queue= Queue()
discovered_subdomains = []

with open("subdomains.txt", "r", encoding="utf-8") as file:
    for line in file:
        in_queue.put(line.strip())


def scan_thread(domain, thred):
    global in_queue
    global out_queue

    while in_queue.qsize():
        subdomain = in_queue.get()
        url = f"http://{subdomain}.{domain}"
        message = f"[Thread: {thred}]"
        try:
            requests.get(url, timeout=2)
        except (requests.ConnectionError, requests.ReadTimeout):
            pass
        else:
            print("[+] Discovered subdomain:", url, message)
            out_queue.put(url)

workers = []
for index in range(1, 101):
    workers.append(Thread(target = scan_thread, args=(domain, index)))

for worker in workers:
    worker.start()

for worker in workers:
    worker.join()

file_name = f"{domain}_discovered_subdomains.txt"
with open(file_name, "w", encoding="utf-8") as f:
    while out_queue.qsize():
        print(out_queue.get(), file = f)
print(f"saved to file {file_name}")
