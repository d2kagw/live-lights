#!/usr/bin/env python
import numpy as np
import cv2, colorsys
import math
import config

PIXEL_SIZE = 3

# Use --------------------------------------
# strip = strip.Strip()
# strip.setColor(bytearray(b'\x0f\x0f\xff'))

class Strip(object):
  def __init__(self):
    super(Strip, self).__init__()
    
    self.spidev = file('/dev/spidev0.0', 'wb')   

    self.pixel_width  = int(math.ceil(float(config.VIDEO_WIDTH) / float(config.STRIP_COLUMNS)))
    self.pixel_height = int(math.ceil(float(config.VIDEO_HEIGHT) / float(config.STRIP_ROWS )))

  def cleanup(self):
    print "Cleaning up SPI..."
    self.spidev.close()

  def process_image(self, image):
    for x in range(0, config.STRIP_COLUMNS):
      for y in range(0, config.STRIP_ROWS):
        px = x * self.pixel_width
        py = y * self.pixel_height
        
        if config.OUTPUT_WINDOW:
          cv2.rectangle(image, (px, py), (px + self.pixel_width, py + self.pixel_width), (0, 0, 0), 1)

    # for led_x in range(0, config.STRIP_COLUMNS):
    #   for led_y in range(0, config.STRIP_ROWS):
    #     if led_x == 0 or led_x == (config.STRIP_COLUMNS-1):
    #       process_pixel()
    #       cv2.rectangle(image, (led_y * pixel_height, led_x * pixel_width), ((led_y+1) * pixel_height, (led_x+1) * pixel_width), (0, 0, 0), 1)
    #     else:
    #       if led_y == 0 or led_y == (config.STRIP_ROWS-1):
    #         cv2.rectangle(image, (led_y * pixel_height, led_x * pixel_width), ((led_y+1) * pixel_height, (led_x+1) * pixel_width), (0, 0, 0), 1)
    #
    return image

  # def process_pixel(self, image, led_x, led_y):
  #   cv2.rectangle(image, (led_y * pixel_height, led_x * pixel_width), ((led_y+1) * pixel_height, (led_x+1) * pixel_width), (0, 0, 0), 1)

  #   return image

  def setColor(self, color):
    index = 0
    output = bytearray(config.STRIP_TOTAL * PIXEL_SIZE + 3)

    for index in range(config.STRIP_TOTAL):
      output[(index * PIXEL_SIZE):] = color
      output += '\x00' * ((config.STRIP_TOTAL - 1 - index) * PIXEL_SIZE)
    
    self.spidev.write(output)
    self.spidev.flush()
