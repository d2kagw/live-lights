#!/usr/bin/env python
import config
import colorsys

PIXEL_SIZE = 3

# Use --------------------------------------
# strip = strip.Strip()
# strip.setColor(bytearray(b'\x0f\x0f\xff'))

class Strip(object):
  def __init__(self):
    super(Strip, self).__init__()
    
    self.spidev = file('/dev/spidev0.0', 'wb')    

  def cleanup(self):
    print "Cleaning up SPI..."
    self.spidev.close()

  def setColor(self, color):
    index = 0
    output = bytearray(config.STRIP_TOTAL * PIXEL_SIZE + 3)

    for index in range(config.STRIP_TOTAL):
      output[(index * PIXEL_SIZE):] = color
      output += '\x00' * ((config.STRIP_TOTAL - 1 - index) * PIXEL_SIZE)
    
    self.spidev.write(output)
    self.spidev.flush()
