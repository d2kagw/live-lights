#!/usr/bin/env python
import numpy as np
import cv2, colorsys
import math
import config

PIXEL_SIZE = 3

class Strip(object):
  def __init__(self):
    super(Strip, self).__init__()
    
    self.spidev = file('/dev/spidev0.0', 'wb')   

  def cleanup(self):
    print "Cleaning up SPI..."
    self.set_color(bytearray("0 0 0"))
    self.spidev.close()

  def set_rgb_color(self, rgb):
    # assumes 0-255 color range in RGB order
    color = bytearray.fromhex('%02x %02x %02x' % (rgb[0], rgb[1], rgb[2]))
    self.set_color(color)

  def set_color(self, color):
    # assumes bytearray
    index = 0
    output = bytearray(config.STRIP_TOTAL * PIXEL_SIZE + 3)

    for index in range(config.STRIP_TOTAL):
      output[(index * PIXEL_SIZE):] = color
      output += '\x00' * ((config.STRIP_TOTAL - 1 - index) * PIXEL_SIZE)
    
    self.spidev.write(output)
    self.spidev.flush()
