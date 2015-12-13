import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

pinRed    = 11
pinYellow = 13

pinRGB_R = 36
pinRGB_G = 38
pinRGB_B = 40

pinSwitch_Left  = 37
pinSwitch_Right = 35

ledPins = [pinRed, pinYellow, pinRGB_R, pinRGB_G, pinRGB_B]
switchPins = [pinSwitch_Left, pinSwitch_Right]

for pin in ledPins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.LOW)

for pin in switchPins:
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def my_callback(channel):
  GPIO.output(pinRed, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(pinRed, GPIO.LOW)

def my_callback2(channel):
  GPIO.output(pinYellow, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(pinYellow, GPIO.LOW)

GPIO.add_event_detect(pinSwitch_Right, GPIO.FALLING, callback=my_callback, bouncetime=300)
GPIO.add_event_detect(pinSwitch_Left, GPIO.FALLING, callback=my_callback2, bouncetime=300)

while True:
  GPIO.output(pinRGB_R, GPIO.HIGH)
  GPIO.output(pinRGB_G, GPIO.LOW)
  time.sleep(0.25)
  GPIO.output(pinRGB_R, GPIO.LOW)
  GPIO.output(pinRGB_G, GPIO.HIGH)
  time.sleep(0.25)
