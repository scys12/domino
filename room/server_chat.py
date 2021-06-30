import socket
import select
import sys
import threading
import pickle, base64
from random import randint


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip_address = 'localhost'
port = 8081
server.bind((ip_address, port))
server.listen(100)
waiting_room = []
rooms = {}

def serialize(msg):
	return msg.encode()

def clientthread(conn, addr):
	while True:
		try:
			msg = conn.recv(2048)
			if msg:
				print('Data recv : {}'.format(msg))
				broadcast_waiting_room(msg)
			else:
				remove(conn)
		except Exception as e:
			print(e)
			continue

def private(msg, dst):
	# print(dst)
	try:
		dst.send(msg)
	except Exception as e:
		print(e)
		remove(dst)
		dst.close()

def broadcast_waiting_room(msg):
	print('Broadcasting ' + msg.decode())
	for c in waiting_room:
		if c:
			print(c)
			try:
				c.send(msg)
				print('Message sent to {}!'.format(str(c)))
			except Exception as e:
				print(e)
				remove(c)
				c.close()

def broadcast_room(msg, room):
	print('Broadcasting ' + msg.decode())
	for c in room:
		if c:
			print(c)
			try:
				c.send(msg)
				print('Message sent to {}!'.format(str(c)))
			except Exception as e:
				print(e)
				remove(c)
				c.close()

def remove(conn):
	for r in rooms:
		if conn in rooms[r]:
			rooms[r].remove(conn)

while True:
	conn, addr = server.accept()
	waiting_room.append(conn)
	if(len(waiting_room) == 1):
		for l in waiting_room:
			private(serialize('Silakan menunggu'), l)
	elif(len(waiting_room) == 2):
		id_room = str(randint(1000, 9999))
		while id_room in rooms:
			id_room = str(randint(1000, 9999))
		rooms[id_room] = waiting_room
		for l in waiting_room:
			private(serialize(f'Anda sudah terpasangkan. ID Room Anda adalah {id_room}'), l)
		waiting_room = []
		print(rooms)
	print(':'.join([str(_) for _ in addr]) + ' connected')
	threading.Thread(target = clientthread, args=(conn, addr)).start()
conn.close()