#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <ifaddrs.h>
#include <netdb.h>

//Kies de port waar je de server op wil hosten
const int PORT = 5000;
//Kies je server wachtwoord
const std::string SERVER_PASSWORD = "11223344";

void printIPAddress() {
    struct ifaddrs *ifaddr, *ifa;

    if (getifaddrs(&ifaddr) == -1) {
        perror("getifaddrs");
        return;
    }

    for (ifa = ifaddr; ifa != nullptr; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr == nullptr)
            continue;
        if (ifa->ifa_addr->sa_family != AF_INET)
            continue;
        char host[NI_MAXHOST];
        int s = getnameinfo(
            ifa->ifa_addr,
            sizeof(struct sockaddr_in),
            host,
            NI_MAXHOST,
            nullptr,
            0,
            NI_NUMERICHOST
        );
        if (s == 0) {
            std::string interface = ifa->ifa_name;
            if (interface != "lo") {
                std::cout << "IP Adres (" << interface << "): "
                          << host << std::endl;
            }
        }
    }

    freeifaddrs(ifaddr);
}

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        std::cerr << "Socket maken mislukt." << std::endl;
        return 1;
    }
    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(PORT);

    if (bind(server_fd, (sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
        std::cerr << "Bind mislukt." << std::endl;
        close(server_fd);
        return 1;
    }
    if (listen(server_fd, 5) < 0) {
        std::cerr << "Listen mislukt." << std::endl;
        close(server_fd);
        return 1;
    }
    std::cout << "SERVER GESTART" << std::endl;
    printIPAddress();
    std::cout << "Poort: " << PORT << std::endl;

    while (true) {
        sockaddr_in clientAddr{};
        socklen_t clientSize = sizeof(clientAddr);

        int client = accept(server_fd,
                            (sockaddr*)&clientAddr,
                            &clientSize);

        if (client < 0)
            continue;

        std::cout << "Nieuwe client verbonden." << std::endl;
        char buffer[1024] = {0};
        int bytes = recv(client, buffer, sizeof(buffer), 0);

        if (bytes <= 0) {
            close(client);
            continue;
        }
        std::string password(buffer);

        while (!password.empty() &&
               (password.back() == '\n' || password.back() == '\r')) {
            password.pop_back();
        }
        if (password != SERVER_PASSWORD) {
            send(client, "LOGIN_FAILED\n", 13, 0);
            close(client);
            continue;
        }
        send(client, "LOGIN_OK\n", 9, 0);
        while (true) {
            memset(buffer, 0, sizeof(buffer));
            bytes = recv(client, buffer, sizeof(buffer), 0);

            if (bytes <= 0)
                break;

            std::cout << buffer;
            std::string reply = "Raspberry Pi zegt: Hallo!\n";
            send(client, reply.c_str(), reply.size(), 0);
        }
        std::cout << "Client verbroken." << std::endl;
        close(client);
    }
    close(server_fd);
    return 0;
}
