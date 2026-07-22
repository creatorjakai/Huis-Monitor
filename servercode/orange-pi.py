import socket

HOST = "0.0.0.0"
PORT = 5000
SERVER_PASSWORD = "11223344"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

print("SERVER GESTART")

while True:

    client, addr = sock.accept()

    print("Verbonden:", addr)

    password = client.recv(1024).decode().strip()

    if password == SERVER_PASSWORD:

        client.sendall(b"LOGIN_OK\n")

        while True:

            data = client.recv(1024)

            if not data:
                break

            print(data.decode().strip())

            client.sendall(b"Orange Pi zegt: Hallo!\n")

    else:

        client.sendall(b"LOGIN_FAILED\n")

    client.close()
