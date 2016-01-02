import numpy as np
import cv2, colorsys

import config

class Mode(object):
  def __init__(self):
    super(Mode, self).__init__()
    
    depth = (config.VIDEO_HEIGHT, config.VIDEO_WIDTH, 3)
    self.image = np.zeros(depth, np.uint8)

  def setup(self):
    pass

  def cleanup(self):
    pass

  def adjust(self):
    pass

  def draw(self):
    return self.image

class ImageMode(Mode):
  def __init__(self):
    super(ImageMode, self).__init__()

    self.index = 0

  def adjust(self):
    self.index += 1
    if self.index >= 3:
      self.index = 0

  def draw(self):
    self.image = cv2.imread('%i.jpg' % self.index, 1)
    return self.image

class FixedColorMode(Mode):
  def __init__(self):
    super(FixedColorMode, self).__init__()

    self.hue = 0.0
    self.increment = 0.1

  def setup(self):
    self.hue = 0.0

  def adjust(self):
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
    self.increment_speeds = [0.1, 0.01, 0.001]
    self.increment_speed = 1

  def setup(self):
    self.hue = 0.0

  def adjust(self):
    self.increment_speed += 1
    if self.increment_speed >= len(self.increment_speeds):
      self.increment_speed = 0

  def draw(self):
    rgb = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
    color = ( int(rgb[1] * 255.0), int(rgb[2] * 255.0), int(rgb[0] * 255.0) )

    cv2.rectangle(self.image, (0, 0), (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), color, -1 )

    self.hue += self.increment_speeds[self.increment_speed]
    if self.hue > 1.0:
      self.hue = 0.0

    return self.image

