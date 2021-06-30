import socket
import select
import sys
import threading
import pickle, base64
from random import randint

from RoomConstants import IP_ADDRESS, PORT, MAX_LISTEN, MAX_RECV


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip_address = IP_ADDRESS
port = PORT
server.bind((ip_address, port))
server.listen(MAX_LISTEN)
waiting_room = []
rooms = {}

def serialize(msg):
	return msg.encode()

def deserialize(msg):
	return msg.decode()

def clientthread(conn, addr):
	while True:
		try:
			msg = conn.recv(MAX_RECV)
			for r in rooms:
				if conn in rooms[r]:
					id_room = r
			if msg:
				# Untuk handling pesan-pesan yang diterima
				if msg.decode() == 'Disconnect':
					remove(conn)
					broadcast_room(serialize("Pasangan Anda disconnect"), rooms[id_room])
				else:
					print('Data recv : {}'.format(deserialize(msg)))
					broadcast_room(msg, rooms[id_room])
			else:
				remove(conn)
		except Exception as e:
			print(e)
			continue

def private(msg, dst):
	try:
		dst.send(msg)
	except Exception as e:
		print(e)
		remove(dst)
		dst.close()

def broadcast_waiting_room(msg):
	print('Broadcasting ' + deserialize(msg))
	for c in waiting_room:
		print(c)
		try:
			c.send(msg)
			print('Message sent to {}!'.format(str(c)))
		except Exception as e:
			print(e)
			remove(c)
			c.close()

def broadcast_room(msg, room):
	print('Broadcasting ' + deserialize(msg))
	for c in room:
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