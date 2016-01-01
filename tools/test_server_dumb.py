import time, socket

# ---------------------

UDP_IP = "192.168.0.255"
UDP_PORT = 11647

FPS = 1.0/24.0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# ---------------------

hue = 0.0

while True:
  print "%0.2f" % (hue)
  sock.sendto("%0.2f" % (hue), (UDP_IP, UDP_PORT))
  hue += 0.01
  if hue > 1.0:
    hue = 0.0
  time.sleep(FPS)
