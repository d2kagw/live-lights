#!/usr/bin/env python
import numpy as np
import cv2, colorsys
import math, random

import config

class BaseAnalyser(object):
  def __init__(self, range_start, range_end):
    super(BaseAnalyser, self).__init__()

    self.start_x = range_start[0]
    self.end_x = range_end[0]

    self.start_y = range_start[1]
    self.end_y = range_end[1]

    self._color = [0, 0, 0]

    self.coverage_x = int(math.ceil((self.end_x - self.start_x) * config.ANALYSIS_COVERAGE))
    self.coverage_y = int(math.ceil((self.end_y - self.start_y) * config.ANALYSIS_COVERAGE))

  def process(self, image):
    return image

  def color(self):
    # color is always 0-255
    [0, 0, 0]


class HueAnalyser(BaseAnalyser):
  def process(self, image):
    r = []
    g = []
    b = []

    for x in range(self.start_x, self.end_x, self.coverage_x):
      for y in range(self.start_y, self.end_y, self.coverage_y):
        r += [image[y][x][2]]
        g += [image[y][x][1]]
        b += [image[y][x][0]]

        if config.OUTPUT_WINDOW:
          cv2.line(image, (x, y), (x, y), (150, 150, 150), 1)

    self._color = [
      np.average(r),
      np.average(g),
      np.average(b)
    ]

    if config.OUTPUT_WINDOW:
      cv2.rectangle(image, (self.start_x, self.start_y), (self.end_x, self.end_y), (150, 150, 150), 1)
    
    return image

  def color(self):
    return self._color
