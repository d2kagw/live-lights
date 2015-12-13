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

pins = [pinRed, pinYellow, pinRGB_R, pinRGB_G, pinRGB_B]

for pin in pins:
  GPIO.setup(pin, GPIO.OUT)

while True:
  for pin in pins:
    GPIO.output(pin, GPIO.HIGH)
  time.sleep(1)
  for pin in pins:
    GPIO.output(pin, GPIO.LOW)
  time.sleep(1)
