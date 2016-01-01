import time

PIXEL_COUNT = 50
PIXEL_SIZE = 3

spidev = file('/dev/spidev0.0', "wb")

output = bytearray(PIXEL_COUNT * PIXEL_SIZE + 3)

colors = [
  bytearray(b'\xff\x0f\x0f'),
  bytearray(b'\x0f\xff\x0f'),
  bytearray(b'\x0f\x0f\xff')
]

while True:
  for color in colors:
    index = 0
    for index in range(PIXEL_COUNT):
      output[(index * PIXEL_SIZE):] = color
      output += '\x00' * ((PIXEL_COUNT - 1 - index) * PIXEL_SIZE)
    print ','.join(format(x, '02x') for x in output)
    spidev.write(output)
    spidev.flush()
    time.sleep(0.5)

