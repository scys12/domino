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

    def stop(self):
        self.done = True

    def connect(self):
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
                sockets_list = [self.server]
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
                            if 'state' in data and data['state'] > 0:
                                self.data = data
                        except StopIteration:
                            pass
                    else:
                        msg = sys.stdin.readline()
                        self.server.send(msg.encode())
            except KeyboardInterrupt:
                self.disconnect()
        self.server.close()

    def disconnect(self):
        msg = {
            'status': 'disconnect'
        }
        self.stop()
        self.send_to_server(msg)

    def send_to_server(self, msg):
        try:
            self.is_waiting = True
            self.is_sending = False
            msg = marshal.dumps(msg)
            self.server.send(msg)
        except:
            pass
