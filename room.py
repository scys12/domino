from player import Player
import uuid
from room_exception import ClientIsNotRegistered, RoomNotFound, NotInRoom
from room_space import RoomSpace

class Room:
    def __init__(self, capacity=2) -> None:
        """ """
        self.rooms = {}
        self.players = {}
        self.roomCapacity = capacity
    
    def registerPlayer(self, addr, udpPort):
      """
      Register player
      """
      player = None
      for registered in self.players.values():
        if registered.addr == addr:
          player = registered
          player.udpAddr((addr[0], udpPort))
          break
      
      if player is None:
        player = Player(addr, udpPort)
        self.players[player.identity] = player

      return player

    def join(self, playerIdentity, roomId=None):
      """
      Add player to room
      """
      if playerIdentity not in self.players:
        raise ClientIsNotRegistered("Player is not registered")

      player = self.players[playerIdentity]
      for roomId in self.rooms.keys():
        if not self.rooms[roomId].is_full():
          self.rooms[roomId].players.append(player)
          return roomId

      roomId = self.create()

    def leave(self, player_identifier, room_id):
      """
      Remove a player from a room
      """
      if player_identifier not in self.players:
          raise ClientIsNotRegistered("Player is not registered")

      player = self.players[player_identifier]

      if room_id in self.rooms:
          self.rooms[room_id].leave(player)
      else:
          raise RoomNotFound()

    def create(self, roomName=None):
      """
      Create a new room
      """
      identifier = str(uuid.uuid4())
      self.rooms[identifier] = Room(identifier, self.room_capacity, room_name)
      return identifier

    def removeEmptyRoom(self):
      """
      Delete empty room
      """
      for roomId in list(self.rooms.keys()):
        if self.rooms[roomId].is_empty():
          del self.rooms[roomId]

    def send(self, identifier, room_id, message, sock):
        """
        Send data to all players in room, except sender
        """
        if room_id not in self.rooms:
            raise RoomNotFound()

        room = self.rooms[room_id]
        if not room.is_in_room(identifier):
            raise NotInRoom()

        for player in room.players:
            if player.identifier != identifier:
                player.send_udp(identifier, message)

    def sendto(self, identifier, room_id, recipients, message, sock):
        """
        Send data to specific player(s)
        """
        if room_id not in self.rooms:
            raise RoomNotFound()

        room = self.rooms[room_id]
        if not room.is_in_room(identifier):
            raise NotInRoom()
   
        if isinstance(recipients, str):
            recipients = [recipients]
            
        for player in room.players:
            if player.identifier in recipients:
                player.send_udp(identifier, message)