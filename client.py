#!/usr/bin/env python3
import socket
import select
import sys


server_address = ("localhost", 8081)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(server_address)

sys.stdout.write(">> ")
try:
    while True:
        sockets_list = [sys.stdin, server]
        read_socket, write_socket, error_socket = select.select(sockets_list, [], [])

        print("debug print")
        print("read socket", read_socket)
        print("write socket", write_socket)
        print("error socket", error_socket)

        for sock in read_socket:
            if sock == server:
                message = sock.recv(2048).decode()
                print(message)
            else:
                message = sys.stdin.readline()
                server.send(message.encode())
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()

except KeyboardInterrupt:
    server.close()
    sys.exit(0)
