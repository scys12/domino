#!/usr/bin/env python3
import socket
import select
import sys
import threading
import re
import ast
import uuid

import socket
import select
import sys
import threading
import re
import ast
import uuid


def clientthread(conn, addr):
    while True:
        try:
            message = conn.recv(2048).decode()
            if message:
                if "private" in message:
                    param = message.split(' ')
                    message_to_send = '<' + addr[0] + '>(Private)' + param[2]
                    privatemessage(message_to_send, param[1])
                else:
                    message_to_send = '<' + addr[0] + '>' + message
                    print(message_to_send)
                    broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue


def privatemessage(message, client_id):
    try:
        conn = client_dict[client_id]
        conn.send(message.encode())
    except:
        client_dict[client_id].close()
        client_dict.pop(client_id)


def broadcast(message, connection):
    for client in client_list:
        if client != connection:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove(client)


def remove(connection):
    if connection in client_list:
        client_list.remove(connection)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = 'localhost'
port = 8081
server.bind((host, port))
server.listen(100)
client_list = []
client_dict = {}

try:
    while True:
        conn, addr = server.accept()
        client_list.append(conn)
        print(addr[0] + ' connected')
        client_id = str(uuid.uuid1())
        conn.send(client_id.encode())
        client_dict[client_id] = conn
        threading.Thread(target=clientthread, args=(conn, addr)).start()

except KeyboardInterrupt:
    server.close()
    sys.exit(0)