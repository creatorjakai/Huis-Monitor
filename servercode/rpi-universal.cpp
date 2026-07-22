#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>

const int PORT = 5000;
const std::string SERVER_PASSWORD = "11223344";

int main() {

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(PORT);

    bind(server_fd, (sockaddr*)&serverAddr, sizeof(serverAddr));

    listen(server_fd, 5);

    std::cout << "SERVER GESTART" << std::endl;

    while (true) {

        sockaddr_in clientAddr{};
        socklen_t clientSize = sizeof(clientAddr);

        int client = accept(server_fd,
                            (sockaddr*)&clientAddr,
                            &clientSize);

        std::cout << "Nieuwe client verbonden." << std::endl;

        char buffer[1024] = {0};

        int bytes = recv(client, buffer, sizeof(buffer), 0);

        if (bytes <= 0) {
            close(client);
            continue;
        }

        std::string password(buffer);

        while (!password.empty() &&
              (password.back() == '\n' || password.back() == '\r'))
            password.pop_back();

        if (password != SERVER_PASSWORD) {

            send(client,
                 "LOGIN_FAILED\n",
                 13,
                 0);

            close(client);
            continue;
        }

        send(client,
             "LOGIN_OK\n",
             9,
             0);

        while (true) {

            memset(buffer, 0, sizeof(buffer));

            bytes = recv(client,
                         buffer,
                         sizeof(buffer),
                         0);

            if (bytes <= 0)
                break;

            std::cout << buffer;

            std::string reply =
                "Raspberry Pi zegt: Hallo!\n";

            send(client,
                 reply.c_str(),
                 reply.size(),
                 0);
        }

        close(client);
    }

    close(server_fd);
}
