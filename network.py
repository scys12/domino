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
        self.status = ""
        # self.start_network()

    def stop(self):
        self.done = True

    def connect(self):
        print("connected")
        try:
            self.server.connect(self.addr)
            print("Connected to %s:%d" % (self.addr[0], self.addr[1]))
            return self.client.recv(2048).decode()
        except:
            pass

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
                            message = data['message']
                            print("pesan {}".format(message))
                            if(type(message) == str):
                              print("is string")
                              if(message.find("Anda sudah terpasangkan")):
                                print("is connected")
                                self.status = "Anda sudah terpasangkan"
                            # print(data)
                        except StopIteration:
                            print("cd")
                    else:
                        msg = sys.stdin.readline()
                        self.server.send(msg.encode())
            except KeyboardInterrupt:
                self.server.send('Disconnect'.encode())
                self.server.close()
                sys.exit(0)
        self.server.close()
