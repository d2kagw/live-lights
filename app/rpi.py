#!/usr/bin/env python
import RPi.GPIO as GPIO

def setup():
  cleanup()
  GPIO.setmode(GPIO.BCM)

def cleanup():
  print "Cleaning up GPIO..."
  GPIO.cleanup()

# ---------------------------

class LEDPin(object):
  def __init__(self, name, pin, use_pwm=False):
    super(LEDPin, self).__init__()
    self.name = name
    self.pin  = pin
    self.uses_pwm = use_pwm
    self.pwm  = False

    print "Setting up pin %s as %s LED" % (pin, name)
    GPIO.setup(self.pin, GPIO.OUT)
    self.off()

    if self.uses_pwm:
      self.pwm = GPIO.PWM(self.pin, 50)
      self.pwm.start(0)

  def on(self):
    GPIO.output(self.pin, GPIO.HIGH)

  def off(self):
    GPIO.output(self.pin, GPIO.LOW)

  def cdc(self, duty):
    self.pwm.ChangeDutyCycle(duty)

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
