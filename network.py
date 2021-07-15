import socket
import select
import sys
import marshal
import threading

from backend.RoomConstants import IP_ADDRESS, PORT, MAX_RECV


class NetworkThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_address = IP_ADDRESS
        self.port = PORT
        self.addr = (self.ip_address, self.port)
        self.daemon = True  # exit with parent
        self.done = False
        self.is_waiting = True
        self.is_sending = False
        self.data = None
        self.data_to_send = None

    def stop(self):
        self.done = True

    def connect(self):
        print("connected")
        try:
            self.server.connect(self.addr)
            print("Connected to %s:%d" % (self.addr[0], self.addr[1]))
            return self.client.recv(2048).decode()
        except:
            print("Connection refused!")

    def run(self):
        self.connect()
        while not self.done:
            try:
                sockets_list = [sys.stdin, self.server]
                read_socket, write_socket, error_socket = select.select(
                    sockets_list, [], [])

                for socks in read_socket:
                    if socks == self.server:
                        msg = socks.recv(MAX_RECV)
                        try:
                            data = marshal.loads(msg)
                            if 'is_waiting' in data:
                                self.is_waiting = data['is_waiting']
                            else:
                                self.is_waiting = False
                                self.is_sending = True
                            self.data = data
                            self.data_to_send = None
                        except StopIteration:
                            print("cd")
                    else:
                        print("abc")
                        msg = sys.stdin.readline()
                        self.server.send(msg.encode())
            except KeyboardInterrupt:
                self.server.send('Disconnect'.encode())
                self.server.close()
                sys.exit(0)
        self.server.close()

    def send_card(self, status, sent_card):
        self.is_waiting = True
        self.is_sending = False
        msg = {
            'status': status,
            'card': sent_card,
        }
        msg = marshal.dumps(msg)
        self.server.send(msg)