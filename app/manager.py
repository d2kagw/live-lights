#!/usr/bin/env python
import numpy as np
import cv2, colorsys
import math, random

import config
import rpi, strip

# ------------------------------    

class Mode(object):
  def __init__(self):
    super(Mode, self).__init__()
    
    depth = (config.VIDEO_HEIGHT, config.VIDEO_WIDTH, 3)
    self.image = np.zeros(depth, np.uint8)

  def setup(self):
    pass

  def cleanup(self):
    pass

  def adjust(self, index):
    pass

  def draw(self):
    return self.image

class FixedColorMode(Mode):
  def __init__(self):
    super(FixedColorMode, self).__init__()

    self.hue = 0.0
    self.increment = 0.1

  def setup(self):
    self.hue = 0.0

  def adjust(self, index):
    if index == 0:
      self.hue -= self.increment
    else:
      self.hue += self.increment

    if self.hue < 0.0:
      self.hue = 1.0

    if self.hue > 1.0:
      self.hue = 0.0

  def draw(self):
    rgb = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
    color = ( int(rgb[1] * 255.0), int(rgb[2] * 255.0), int(rgb[0] * 255.0) )

    cv2.rectangle(self.image, (0, 0), (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), color, -1 )

    return self.image

class CyclingColorMode(Mode):
  def __init__(self):
    super(CyclingColorMode, self).__init__()

    self.hue = 0.0
    self.increment = 0.05

  def setup(self):
    self.hue = 0.0

  def draw(self):
    rgb = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
    color = ( int(rgb[1] * 255.0), int(rgb[2] * 255.0), int(rgb[0] * 255.0) )

    cv2.rectangle(self.image, (0, 0), (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), color, -1 )

    self.hue += self.increment
    if self.hue > 1.0:
      self.hue = 0.0

    return self.image

# ------------------------------

class Manager(object):
  def __init__(self):
    super(Manager, self).__init__()
    
    self.strip = strip.Strip()
    self.rgb_a = config.RPI_RGB_LEDS[0]
    self.rgb_b = config.RPI_RGB_LEDS[1]

    self.modes = [
      FixedColorMode(),
      CyclingColorMode()
    ]

    self.mode = False
    self.mode_index = 1
    self.toggle(self.mode_index)

    self.window = False

  def toggle(self, mode_index = False):
    if mode_index is not False:
      self.mode_index = mode_index
    else:  
      self.mode_index += 1
    
    if self.mode_index >= len(self.modes):
      self.mode_index = 0

    if self.mode is not False:
      self.mode.cleanup()

    self.mode = self.modes[self.mode_index]
    print "Setting mode to: %s" % self.mode

    self.mode.setup()

  def adjust_a(self):
    self.mode.adjust(0)

  def adjust_b(self):
    self.mode.adjust(1)

  def go(self):
    image = self.mode.draw()

    if config.OUTPUT_SURROUND:
      image = self.rgb_a.process_image(image)
      image = self.rgb_b.process_image(image)

    if config.OUTPUT_STRIP:
      image = self.strip.process_image(image)

    if config.OUTPUT_WINDOW:
      self.window = cv2.imshow('LiveLights', image)
      self.window = cv2.waitKey(int(config.FPS * 1000))
