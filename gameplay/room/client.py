import socket
import select
import sys
import marshal

from RoomConstants import IP_ADDRESS, PORT, MAX_RECV

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = IP_ADDRESS
port = PORT
server.connect((ip_address, port))

while True:
	try:
		sockets_list = [sys.stdin, server]
		read_socket, write_socket, error_socket = select.select(sockets_list, [], [])

		for socks in read_socket:
			if socks == server:
				msg = socks.recv(MAX_RECV)
				try:
						data = marshal.loads(msg)
						print(data)
				except EOFError:
						print(msg.decode())				
			else:
				msg = sys.stdin.readline()
				server.send(msg.encode())
	except KeyboardInterrupt:
		server.send('Disconnect'.encode())
		server.close()
		sys.exit(0)

server.close()