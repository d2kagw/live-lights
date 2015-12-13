import RPi.GPIO as GPIO
import time, math, random, socket

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

# ---------------------

UDP_IP = "192.168.0.255"
UDP_PORT = 11647

FPS = 1.0/12.0

pinRed    = 11
pinYellow = 13

pinRGB_R = 36
pinRGB_G = 38
pinRGB_B = 40

pinSwitch_Left  = 37
pinSwitch_Right = 35

# ---------------------

ledPins = [pinRed, pinYellow, pinRGB_R, pinRGB_G, pinRGB_B]
switchPins = [pinSwitch_Left, pinSwitch_Right]

# ---------------------

for pin in ledPins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.LOW)

for pin in switchPins:
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ---------------------

def toggleRedLED(channel):
  GPIO.output(pinRed, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(pinRed, GPIO.LOW)

def toggleYellowLED(channel):
  GPIO.output(pinYellow, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(pinYellow, GPIO.LOW)

GPIO.add_event_detect(pinSwitch_Right, GPIO.FALLING, callback=toggleRedLED, bouncetime=300)
GPIO.add_event_detect(pinSwitch_Left, GPIO.FALLING, callback=toggleYellowLED, bouncetime=300)

# ---------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# ---------------------

rgbR = GPIO.PWM(pinRGB_R, 50)
rgbR.start(0)

rgbG = GPIO.PWM(pinRGB_G, 50)
rgbG.start(0)

rgbB = GPIO.PWM(pinRGB_B, 50)
rgbB.start(0)

r = 0.0
g = 0.5
b = 0.99

while True:
  rVal = (math.sin(r)*50)+50
  rgbR.ChangeDutyCycle(rVal)

  gVal = (math.cos(g)*50)+50
  rgbG.ChangeDutyCycle(gVal)

  bVal = (math.sin(b)*50)+50
  rgbB.ChangeDutyCycle(bVal)

  r += 0.01
  g += 0.02
  b += 0.03

  message = "%i,%i,%i" % ( ((rVal/100)*255), ((gVal/100)*255), ((bVal/100)*255) )
  sock.sendto(message, (UDP_IP, UDP_PORT))

  time.sleep(FPS)
