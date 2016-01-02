#!/usr/bin/env python
import colorsys
import socket
import config

class Broadcast(object):
  def __init__(self):
    super(Broadcast, self).__init__()

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

  def send(self, rgb):
    message = "%i,%i,%i" % (rgb[0], rgb[1], rgb[2])
    self.sock.sendto(message, (config.UDP_IP, config.UDP_PORT))

# class Listen(object):
#   
# XXX: TODO
