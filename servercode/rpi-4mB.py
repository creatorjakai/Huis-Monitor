import socket

HOST = "0.0.0.0"
PORT = 5000
SERVER_PASSWORD = "11223344"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("SERVER GESTART")

while True:

    client, addr = server.accept()

    print("Nieuwe client:", addr)

    try:

        client.settimeout(5)

        password = client.recv(1024).decode().strip()

        if password == SERVER_PASSWORD:

            client.sendall(b"LOGIN_OK\n")

            while True:

                data = client.recv(1024)

                if not data:
                    break

                print(data.decode().strip())

                client.sendall(b"Raspberry Pi 4 zegt: Hallo!\n")

        else:

            client.sendall(b"LOGIN_FAILED\n")

    finally:
        client.close()
