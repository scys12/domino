import socket
import time
import argparse
from threading import Thread, Lock
from room import Room

def main():
  """
  Start udp and tcp
  """
  pass

def createUDP(Thread):
  pass

def createTCP(Thread):
  pass

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Server')
  parser.add_argument('--tcpport', dest='tcp_port', help='tcp port', default='5000')
  parser.add_argument('--udpport', dest='udp_port', help='udp port', default='5000')

  arguments = parser.parse_args()
  roomInstance = Room()