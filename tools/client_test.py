import numpy as np
import cv2
import time
import socket

UDP_IP = "192.168.0.255"
UDP_PORT = 11647

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

img = np.zeros((100,100,3), np.uint8)

while True:
  data, addr = sock.recvfrom(12)
  color = data.split(',')
  color = (float(color[1]), float(color[2]), float(color[0]))
  cv2.rectangle(img, (0, 0), (100,100), color, -1, 4 );
  v = cv2.imshow('image', img)
  v = cv2.waitKey(1)
