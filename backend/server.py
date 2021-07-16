import socket
import select
import sys
import threading
import pickle
import base64
from random import randint
from .player import Player
from .board import Board
import marshal

from .RoomConstants import IP_ADDRESS, PORT, MAX_LISTEN, MAX_RECV


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


def create_message_dict(msg):
    return {
        'message': msg
    }


def serialize_marshal(data):
    return marshal.dumps(data)


def deserialize(msg):
    return msg.decode()


def deserialize_marshal(data):
    return marshal.loads(data)


def is_game_finished(pivot_card_left, pivot_card_right, list_players):
    is_game_finished = True
    for player in list_players:
        for card in player.cards:
            if (pivot_card_left['direction'] == 'left' and pivot_card_left['top'] in card) \
                    or (pivot_card_left['direction'] == 'right' and pivot_card_left['down'] in card) \
                    or (pivot_card_right['direction'] == 'left' and pivot_card_right['down'] in card) \
                    or (pivot_card_right['direction'] == 'right' and pivot_card_right['top'] in card) \
                    or (pivot_card_left['direction'] == 'top' and (pivot_card_left['top'] in card or pivot_card_left['down'] in card)) \
                    or (pivot_card_right['direction'] == 'top' and (pivot_card_right['top'] in card or pivot_card_right['down'] in card)):
                is_game_finished = False
    return is_game_finished


def cards_value_of_player(board, player):
    total = 0
    for card in player.cards:
        total += board.value[card]
    return total


def save_highscore(player, enemy_player):
    text = '{}({}) - ({}){}\n'.format(player.username, player.total_value,
                                      enemy_player.total_value, enemy_player.username)
    f = open("highscore.txt", "a+")
    highscore = f.write(text)


def clientthread(player, addr):
    id_room = None
    running = True
    while running:
        try:
            msg = player.connect.recv(MAX_RECV)
            marshaled_msg = deserialize_marshal(msg)
            for room_id in rooms:
                if player in rooms[room_id][1]:
                    id_room = room_id
            if marshaled_msg:
                # Untuk handling pesan-pesan yang diterima
                if 'status' in marshaled_msg and marshaled_msg['status'] == 'disconnect':
                    remove(player)
                    msg = {
                        'state': -1,
                        'message': 'Lawan meninggalkan game'
                    }
                    broadcast_room(
                        serialize_marshal(msg), rooms[id_room]
                    )
                    running = False
                else:
                    if 'status' in marshaled_msg and marshaled_msg['status'] == 'send_username':
                        board, list_players, chat_history = rooms[id_room]
                        player.username = marshaled_msg['username']
                        if list_players[0].identifier == player.identifier:
                            rooms[id_room] = (
                                board, [player, list_players[1]], chat_history)
                        else:
                            rooms[id_room] = (
                                board, [list_players[0], player], chat_history)
                            enemy_player = list_players[0]
                        game_state = {
                            'state': 0,
                            'message': True,
                        }
                        broadcast_room(serialize_marshal(
                            game_state), rooms[id_room])
                    elif 'status' in marshaled_msg and marshaled_msg['status'] == 'send_card':
                        card_data = marshaled_msg['card']
                        board, list_players, chat_history = rooms[id_room]
                        board.update_board(card_data)
                        player.throw_card(card_data['top'], card_data['down'])

                        if list_players[0].identifier == player.identifier:
                            rooms[id_room] = (
                                board, [player, list_players[1]], chat_history)
                            enemy_player = list_players[1]
                        else:
                            rooms[id_room] = (
                                board, [list_players[0], player], chat_history)
                            enemy_player = list_players[0]

                        if len(player.cards) == 0:
                            enemy_player.total_value = cards_value_of_player(
                                board, enemy_player)
                            player.total_value = cards_value_of_player(
                                board, player)

                            save_highscore(player, enemy_player)

                            game_state = {
                                'state': 4,
                                'winner': player.identifier,
                                'my_value': player.total_value,
                                'enemy_value': enemy_player.total_value,
                                'enemy_username': enemy_player.username,
                                'board': board.serialize_data(player.status),
                                'player': player.serialize_data(),
                            }
                            private(serialize_marshal(game_state), player)
                            game_state['player'] = enemy_player.serialize_data()
                            game_state['board'] = board.serialize_data(
                                enemy_player.status)
                            game_state['my_value'] = enemy_player.total_value
                            game_state['enemy_value'] = player.total_value
                            game_state['enemy_username'] = player.username
                            private(serialize_marshal(
                                game_state), enemy_player)
                        elif is_game_finished(marshaled_msg['pivot_card_left'], marshaled_msg['pivot_card_right'], list_players):
                            enemy_player.total_value = cards_value_of_player(
                                board, enemy_player)
                            player.total_value = cards_value_of_player(
                                board, player)

                            save_highscore(player, enemy_player)

                            game_state = {
                                'state': 4,
                                'my_value': player.total_value,
                                'enemy_value': enemy_player.total_value,
                                'enemy_username': enemy_player.username,
                                'board': board.serialize_data(player.status),
                                'player': player.serialize_data(),
                            }
                            if player.total_value >= enemy_player.total_value:
                                game_state['winner'] = enemy_player.identifier
                            else:
                                game_state['winner'] = player.identifier
                            private(serialize_marshal(game_state), player)
                            game_state['player'] = enemy_player.serialize_data()
                            game_state['board'] = board.serialize_data(
                                enemy_player.status)
                            game_state['my_value'] = enemy_player.total_value
                            game_state['enemy_value'] = player.total_value
                            game_state['enemy_username'] = player.username
                            private(serialize_marshal(
                                game_state), enemy_player)
                        else:
                            game_state = {
                                'board': board.serialize_data(player.status),
                                'state': 2,
                                'player': player.serialize_data(),
                            }
                            private(serialize_marshal(game_state), player)
                            game_state['player'] = enemy_player.serialize_data()
                            game_state['board'] = board.serialize_data(
                                enemy_player.status)
                            private(serialize_marshal(
                                game_state), enemy_player)
                    elif 'status' in marshaled_msg and marshaled_msg['status'] == 'time_out':
                        board, list_players, chat_history = rooms[id_room]
                        board.update_turn()
                        if list_players[0].identifier == player.identifier:
                            rooms[id_room] = (
                                board, [player, list_players[1]], chat_history)
                            enemy_player = list_players[1]
                        else:
                            rooms[id_room] = (
                                board, [list_players[0], player], chat_history)
                            enemy_player = list_players[0]

                        if len(player.cards) == 0:
                            enemy_player.total_value = cards_value_of_player(
                                board, enemy_player)
                            player.total_value = cards_value_of_player(
                                board, player)

                            save_highscore(player, enemy_player)

                            game_state = {
                                'state': 4,
                                'winner': player.identifier,
                                'my_value': player.total_value,
                                'enemy_value': enemy_player.total_value,
                                'enemy_username': enemy_player.username,
                                'board': board.serialize_data(player.status),
                                'player': player.serialize_data(),
                            }
                            private(serialize_marshal(game_state), player)
                            game_state['player'] = enemy_player.serialize_data()
                            game_state['board'] = board.serialize_data(
                                enemy_player.status)
                            game_state['my_value'] = enemy_player.total_value
                            game_state['enemy_value'] = player.total_value
                            game_state['enemy_username'] = player.username
                            private(serialize_marshal(
                                game_state), enemy_player)
                        elif is_game_finished(marshaled_msg['pivot_card_left'], marshaled_msg['pivot_card_right'], list_players):
                            enemy_player.total_value = cards_value_of_player(
                                board, enemy_player)
                            player.total_value = cards_value_of_player(
                                board, player)

                            save_highscore(player, enemy_player)

                            game_state = {
                                'state': 4,
                                'my_value': player.total_value,
                                'enemy_value': enemy_player.total_value,
                                'enemy_username': enemy_player.username,
                                'board': board.serialize_data(player.status),
                                'player': player.serialize_data(),
                            }
                            if player.total_value >= enemy_player.total_value:
                                game_state['winner'] = enemy_player.identifier
                            else:
                                game_state['winner'] = player.identifier
                            private(serialize_marshal(game_state), player)
                            game_state['player'] = enemy_player.serialize_data()
                            game_state['board'] = board.serialize_data(
                                enemy_player.status)
                            game_state['my_value'] = enemy_player.total_value
                            game_state['enemy_value'] = player.total_value
                            game_state['enemy_username'] = player.username
                            private(serialize_marshal(
                                game_state), enemy_player)
                        else:
                            game_state = {
                                'board': board.serialize_data(player.status),
                                'state': 2,
                                'player': player.serialize_data(),
                            }
                            private(serialize_marshal(game_state), player)
                            game_state['player'] = enemy_player.serialize_data()
                            game_state['board'] = board.serialize_data(
                                enemy_player.status)
                            private(serialize_marshal(
                                game_state), enemy_player)
                    elif 'status' in marshaled_msg and marshaled_msg['status'] == 'send_msg':
                        board, list_players, chat_history = rooms[id_room]

                        chat_history.append(
                            (player.identifier, marshaled_msg['chat'], marshaled_msg['username']))

                        rooms[id_room] = (board, list_players, chat_history)

                        game_state = {
                            'state': 3,
                            'messages': chat_history[-10:]
                        }
                        broadcast_room(serialize_marshal(
                            game_state), rooms[id_room])
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
    for c in waiting_room:
        try:
            c.connect.send(msg)
            print("Message sent to {}!".format(str(c)))
        except Exception as e:
            print(e)
            remove(c)
            c.connect.close()


def broadcast_room(msg, room):
    for c in room[1]:
        try:
            c.connect.send(msg)
            print("Message sent to {}!".format(str(c)))
        except Exception as e:
            print(e)
            remove(c)
            c.connect.close()


def remove(player):
    for room_id in rooms:
        if player in rooms[room_id][1]:
            rooms[room_id][1].remove(player)


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
                message = create_message_dict("Silakan menunggu")
                message['is_waiting'] = True
                private(serialize_marshal(message), player)
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
            board.init_board()
            chat_history = []
            rooms[id_room] = (board, waiting_room, chat_history)
            for player in waiting_room:
                if player.status == "player1":
                    player.draw_card(board.player1_cards)
                else:
                    player.draw_card(board.player2_cards)

                message = f"Anda sudah terpasangkan. ID Room Anda adalah {id_room}"
                start_game_state = {
                    'message': message,
                    'player': player.serialize_data(),
                    'board': board.serialize_data(player.status),
                    'state': 1,
                    'is_waiting': False
                }
                start_game_state_marshal = serialize_marshal(start_game_state)
                private(
                    start_game_state_marshal,
                    player
                )
            waiting_room = []
            print(rooms)
        print(":".join([str(_) for _ in addr]) + " connected")
        threading.Thread(target=clientthread, args=(
            player_instance, addr)).start()

    conn.close()


if __name__ == '__main__':
    main()
