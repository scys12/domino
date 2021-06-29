from room_exception import RoomFull, NotInRoom

class RoomSpace:
  def __init__(self, identity, capacity, name) -> None:
      """
      Create a new room on server
      """
      self.identity = identity
      self.capacity = capacity
      self.players = []
      if name is not None:
        self.roomName = name
      else:
        self.roomName = identity

  def join(self, player):
    """
    Add player to room
    """
    if not self.is_full():
      self.players.append(player)
    else:
      raise RoomFull("Room is full")

  def leave(self, player):
    """
    Remove player from room
    """
    if player in self.players:
      self.players.remove(player)
    else:
      raise NotInRoom("Player is not in room")

  def empty(self):
    """
    Check if room is empty or not
    """
    if len(self.players) == 0:
      return True
    else:
      return False

  def is_full(self):
    """
    Check if room is full or not
    """
    if len(self.players) == self.capacity:
      return True
    else:
      return False

  def inRoom(self, playerUUID):
    """
    Check if player in room
    """
    inRoom = False
    for player in self.players:
      if player.identity == playerUUID:
        inRoom = True
        break
    return inRoom 