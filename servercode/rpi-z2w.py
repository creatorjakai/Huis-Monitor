import socket

HOST = ""
PORT = 5000
SERVER_PASSWORD = "11223344"

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

print("SERVER GESTART")

while True:

    client, addr = server.accept()

    print(addr)

    password = client.recv(1024).decode().strip()

    if password != SERVER_PASSWORD:
        client.send(b"LOGIN_FAILED\n")
        client.close()
        continue

    client.send(b"LOGIN_OK\n")

    while True:

        data = client.recv(1024)

        if not data:
            break

        print(data.decode().strip())

        client.send(b"Pi Zero 2 W zegt: Hallo!\n")

    client.close()
