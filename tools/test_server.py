import RPi.GPIO as GPIO
import time, socket
import colorsys

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

# ---------------------

UDP_IP = "192.168.0.255"
UDP_PORT = 11647

FPS = 1.0/24.0

pinRed    = 11
pinYellow = 13

pinRGB_R = 36
pinRGB_G = 38
pinRGB_B = 40

pinSwitch_Left  = 37
pinSwitch_Right = 35

# ---------------------

INC_speeds = [0.001, 0.01, 0.1]
INC_speed  = 0
INC_active = True

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

  global INC_active
  INC_active = INC_active == False

  time.sleep(0.1)
  GPIO.output(pinRed, GPIO.LOW)

def toggleYellowLED(channel):
  GPIO.output(pinYellow, GPIO.HIGH)
  
  global INC_speed
  INC_speed += 1
  if INC_speed > 2:
    INC_speed = 0

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

hue = 0.0

while True:
  color = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
  rgbR.ChangeDutyCycle(int(color[0]))
  rgbG.ChangeDutyCycle(int(color[1]))
  rgbB.ChangeDutyCycle(int(color[2]))

  message = "%i,%i,%i" % ( rVal*255, gVal*255, bVal*255 )
  sock.sendto(message, (UDP_IP, UDP_PORT))

  if INC_active:
    hue += INC_speeds[INC_speed]
    if hue > 1.0:
      hue = 0.0

  time.sleep(FPS)
