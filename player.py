import uuid
import socket
import pickle

class Player:
  def __init__(self, addr, udpPort) -> None:
      """
      Identify remote player
      """

      self.identity = str(uuid.uuid4())
      self.addr = addr
      self.udpAddr = (addr[0], int(udpPort))
      self.messageBuilder = []

  def sendTCP(self, success, data, sock):
    """
    Server interaction
    """
    successStr = "False"
    if success:
      successStr = "True"
    
    self.messageBuilder.append({
      "success": successStr,
      "message": data
    })

    messageSend = pickle.dumps(self.messageBuilder)
    sock.send(messageSend.encode())

  def sendUDP(self, playerIdentity, message):
    """
    Game logic interaction 
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    msgDict = {}
    msgDict[playerIdentity] = message

    self.messageBuilder.append(msgDict)
    messageSend = pickle.dumps(self.messageBuilder)
    
    sock.sendto(messageSend.encode(), self.udpAddr)