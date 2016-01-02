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
  
  def on(self):
    for channel in self.pwm:
      self.pwm[channel].start(100)

  def off(self):
    for channel in self.pwm:
      self.pwm[channel].start(0)

  def set_color(self, color):
    # assumes 0-255 color range in RGB order
    self.pwm['r'].ChangeDutyCycle(np.interp(color[0], [0,255], [0,100]))
    self.pwm['g'].ChangeDutyCycle(np.interp(color[1], [0,255], [0,100]))
    self.pwm['b'].ChangeDutyCycle(np.interp(color[2], [0,255], [0,100]))

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
