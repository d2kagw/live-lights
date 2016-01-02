#!/usr/bin/env python
import config, cv2, time
import rpi, strip, modes, analysers, network

class Manager(object):
  def __init__(self):
    super(Manager, self).__init__()
    
    self.strip = strip.Strip()
    self.rgb_a = config.RPI_RGB_LEDS[0]
    self.rgb_b = config.RPI_RGB_LEDS[1]

    self.modes = [
      modes.FixedColorMode(),
      modes.CyclingColorMode()
    ]

    self.mode = False
    self.mode_index = 1
    self.toggle(self.mode_index)

    self.window = False

    self.network = network.Broadcast()

    self.analyser = analysers.HueAnalyser((0, 0), (config.VIDEO_WIDTH, config.VIDEO_HEIGHT))

  def cleanup(self): 
    self.strip.cleanup()

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

    self.analyser.process(image)

    if config.OUTPUT_SURROUND:
      self.rgb_a.set_color(self.analyser.color())
      self.rgb_b.set_color(self.analyser.color())
      self.network.send(self.analyser.color())
    
    if config.OUTPUT_STRIP:
      self.strip.set_rgb_color(self.analyser.color())

    if config.OUTPUT_WINDOW:
      self.window = cv2.imshow('LiveLights', image)
      self.window = cv2.waitKey(int(config.FPS * 1000))
    else:
      time.sleep(config.FPS)

