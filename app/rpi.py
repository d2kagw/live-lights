#!/usr/bin/env python
import RPi.GPIO as GPIO
import numpy as np
import cv2, colorsys
import config
import math

def setup():
  cleanup()
  GPIO.setmode(GPIO.BCM)

def cleanup():
  print "Cleaning up GPIO..."
  GPIO.cleanup()

# ---------------------------

class LEDPin(object):
  def __init__(self, name, pin):
    super(LEDPin, self).__init__()
    self.name = name
    self.pin  = pin

    print "Setting up pin %s as %s LED" % (pin, name)
    GPIO.setup(self.pin, GPIO.OUT)
    self.off()

  def on(self):
    GPIO.output(self.pin, GPIO.HIGH)

  def off(self):
    GPIO.output(self.pin, GPIO.LOW)

# ---------------------------

class RGBPin(object):
  def __init__(self, name, pin_r, pin_g, pin_b):
    super(RGBPin, self).__init__()
    self.name = name
    self.pins = {
      'r': pin_r,
      'g': pin_g,
      'b': pin_b
    }
    self.pwm = {
      'r': False,
      'g': False,
      'b': False
    }

    print "Setting up pins %s as %s RGB" % (self.pins, name)
    
    for channel in self.pins:
      GPIO.setup(self.pins[channel], GPIO.OUT)
      self.pwm[channel] = GPIO.PWM(self.pins[channel], 50)
      self.pwm[channel].start(0)
    
    self.off()
      
  def process_image(self, image):
    r = []
    g = []
    b = []

    coverage = abs(config.ANALYSIS_COVERAGE - 1.0)
    coverage_x = int(config.VIDEO_WIDTH * coverage)
    coverage_y = int(config.VIDEO_HEIGHT * coverage)

    for x in range(0, config.VIDEO_HEIGHT, coverage_x):
      for y in range(0, config.VIDEO_WIDTH, coverage_y):
        r += [image[x][y][2]]
        g += [image[x][y][1]]
        b += [image[x][y][0]]

        if config.OUTPUT_WINDOW:
          cv2.line(image, (y, x), (y+1, x), (0, 0, 0), 1)

    r = np.interp(np.average(r), [0,255], [0,100])
    g = np.interp(np.average(g), [0,255], [0,100])
    b = np.interp(np.average(b), [0,255], [0,100])

    self.color([r, g, b])

    if config.OUTPUT_WINDOW:
      cv2.rectangle(image, (0, 0), (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), (0, 0, 0), 4)

    return image

  def on(self):
    for channel in self.pwm:
      self.pwm[channel].start(100)

  def off(self):
    for channel in self.pwm:
      self.pwm[channel].start(0)

  def color(self, color):
    self.pwm['r'].ChangeDutyCycle(color[0])
    self.pwm['g'].ChangeDutyCycle(color[1])
    self.pwm['b'].ChangeDutyCycle(color[2])

# ---------------------------

class SwitchPin(object):
  def __init__(self, name, pin):
    super(SwitchPin, self).__init__()
    self.name = name
    self.pin  = pin
    self.callback = False

    print "Setting up pin %s as %s Switch" % (pin, name)
    GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.event, bouncetime=300)

  def event(self, _):
    print "Button `%s` clicked" % (self.name)
    if self.callback is not False:
      self.callback()

  def click(self, callback):
    self.callback = callback
