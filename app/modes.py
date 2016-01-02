import numpy as np
import cv2, colorsys

import config

class Mode(object):
  def __init__(self):
    super(Mode, self).__init__()
    
    depth = (config.WINDOW_HEIGHT, config.WINDOW_WIDTH, 3)
    print "DEPTH"
    print depth

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
    self.increment = 0.01

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

