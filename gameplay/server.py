from board import Board
import socket
import select
import sys
import threading
import pickle, base64
from random import randint
from player import Player
import marshal

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


def clientthread(player, addr):
    id_room = None
    while True:
        try:
            msg = player.connect.recv(MAX_RECV)
            for room_id in rooms:
                if player in rooms[room_id]:
                    id_room = room_id
            if msg:
                # Untuk handling pesan-pesan yang diterima
                if msg.decode() == "Disconnect":
                    remove(player)
                    broadcast_room(
                        serialize("Pasangan Anda disconnect"), rooms[id_room]
                    )
                else:
                    print("Data recv : {}".format(deserialize(msg)))
                    broadcast_room(msg, rooms[id_room])
            else:
                remove(player)
        except Exception as e:
            print(e)
            continue


def private(msg, player):
    try:
        player.connect.send(msg)
    except Exception as e:
        print(e)
        remove(player)
        player.connect.close()


def broadcast_waiting_room(msg):
    print("Broadcasting " + deserialize(msg))
    for c in waiting_room:
        print(c)
        try:
            c.send(msg)
            print("Message sent to {}!".format(str(c)))
        except Exception as e:
            print(e)
            remove(c)
            c.close()


def broadcast_room(msg, room):
    print("Broadcasting " + deserialize(msg))
    for c in room:
        print(c)
        try:
            c.send(msg)
            print("Message sent to {}!".format(str(c)))
        except Exception as e:
            print(e)
            remove(c)
            c.close()


def remove(player):
    for room_id in rooms:
        if player in rooms[room_id]:
            rooms[room_id].remove(player)


def main():
    global waiting_room
    while True:
        """
        Accept new connection and create player
        """
        conn, addr = server.accept()
        player_instance = Player(conn)
        waiting_room.append(player_instance)

        # Waiting for player 2
        if len(waiting_room) == 1:
            for player in waiting_room:
                player_instance.set_player_status("player1")
                private(serialize("Silakan menunggu"), player)
        # Second player has been found
        elif len(waiting_room) == 2:
            player_instance.set_player_status("player2")
            id_room = str(randint(1000, 9999))
            while id_room in rooms:
                id_room = str(randint(1000, 9999))
            # create board
            board = Board()
            board.generate_card("player2")
            """
              list card player 1 5 kartu
              list card player 2 4 kartu
              card yang muncul pertama kali
            """

            rooms[id_room] = (board, waiting_room)
            for player in waiting_room:
                if player.status == "player1":
                    player.draw_card(board.player1_cards)
                else:
                  player.draw_card(board.player2_cards)

                message = f"Anda sudah terpasangkan. ID Room Anda adalah {id_room}"
                start_game_state = {
                    'message' : message,
                    'player' : player.serialize_data(),
                    'board' : board.serialize_data(),
                }
                start_game_state_marshal = marshal.dumps(start_game_state)
                private(
                    start_game_state_marshal,
                    player
                )
            waiting_room = []
            print(rooms)
        print(":".join([str(_) for _ in addr]) + " connected")
        threading.Thread(target=clientthread, args=(player_instance, addr)).start()

    conn.close()
