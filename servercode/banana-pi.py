import socket

HOST = "0.0.0.0"
PORT = 5000
SERVER_PASSWORD = "11223344"

server = socket.socket()
server.bind((HOST, PORT))
server.listen(5)

print("SERVER GESTART")

while True:

    client, address = server.accept()

    print(address)

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

        client.send(b"Banana Pi zegt: Hallo!\n")

    client.close()
