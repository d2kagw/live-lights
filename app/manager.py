#!/usr/bin/env python
import config, cv2, time, math
import rpi, strip, modes, analysers, network

class Manager(object):
  def __init__(self):
    super(Manager, self).__init__()
    
    self.strip = strip.Strip()
    self.rgb_a = config.RPI_RGB_LEDS[0]
    self.rgb_b = config.RPI_RGB_LEDS[1]

    # Mode 0 = analysis for each pixel
    # Mode 1 = analysis of whole screen
    self.analyser_mode = 1

    self.image_modes = [
      modes.ImageMode(),
      modes.FixedColorMode(),
      modes.CyclingColorMode()
    ]

    self.image_mode = False
    self.image_mode_index = 0
    self.toggle(self.image_mode_index)

    self.window = False

    self.network = network.Broadcast()

    self.surround_analyser = analysers.HueAnalyser((0, 0), (config.VIDEO_WIDTH, config.VIDEO_HEIGHT))

    self.strip_analysers = []    
    analyser_width  = int(math.ceil(config.VIDEO_WIDTH  / config.STRIP_COLUMNS))
    analyser_height = int(math.ceil(config.VIDEO_HEIGHT / config.STRIP_ROWS))

    for row in range(0, config.STRIP_ROWS):
      if row == 0 or row == config.STRIP_ROWS-1:
        for column in range(0, config.STRIP_COLUMNS):
          a = analysers.HueAnalyser((analyser_width * column, analyser_height * row), (analyser_width * (column + 1), analyser_height * (row + 1)))
          self.strip_analysers += [a]
      else:
        for column in range(0, config.STRIP_COLUMNS, config.STRIP_COLUMNS-1):
          a = analysers.HueAnalyser((analyser_width * column, analyser_height * row), (analyser_width * (column + 1), analyser_height * (row + 1)))
          self.strip_analysers += [a]

  def cleanup(self): 
    self.strip.cleanup()

  def toggle(self, image_mode_index = False):
    if image_mode_index is not False:
      self.image_mode_index = image_mode_index
    else:  
      self.image_mode_index += 1
    
    if self.image_mode_index >= len(self.image_modes):
      self.image_mode_index = 0

    if self.image_mode is not False:
      self.image_mode.cleanup()

    self.image_mode = self.image_modes[self.image_mode_index]
    print "Setting image_mode to: %s" % self.image_mode

    self.image_mode.setup()

  def adjust_a(self):
    self.image_mode.adjust(0)

  def adjust_b(self):
    self.image_mode.adjust(1)

  def go(self):
    image = self.image_mode.draw()

    self.surround_analyser.process(image)

    if config.OUTPUT_SURROUND:
      self.rgb_a.set_color(self.surround_analyser.color())
      self.rgb_b.set_color(self.surround_analyser.color())
      
      self.network.send(self.surround_analyser.color())
    
    if config.OUTPUT_STRIP:
      if self.analyser_mode == 0:
        self.strip.set_rgb_color(self.surround_analyser.color())
      else:
        strip_color = []
        for analyser in self.strip_analysers:
          analyser.process(image)
          rgb = analyser.color()
          strip_color += [rgb]

        self.strip.set_colors(strip_color)

    if config.OUTPUT_WINDOW:
      self.window = cv2.imshow('Live Lights', image)
      self.window = cv2.waitKey(int(config.FPS * 1000))
    else:
      time.sleep(config.FPS)

