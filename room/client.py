import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = 'localhost'
port = 8081
server.connect((ip_address, port))

while True:
	try:
		sockets_list = [sys.stdin, server]
		read_socket, write_socket, error_socket = select.select(sockets_list, [], [])

		for socks in read_socket:
			if socks == server:
				msg = socks.recv(4096)
				print(msg.decode())
			else:
				msg = sys.stdin.readLine()
				server.send(msg.encode())
				print(msg)
	except KeyboardInterrupt:
		server.send('Disconnect'.encode())
		server.close()
		sys.exit(0)

server.close()