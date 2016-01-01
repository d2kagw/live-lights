import RPi.GPIO as GPIO
import time
import colorsys
import socket


# CONSTANTS
# -------------------------------------
PINS = {
  'rgb_1_r': 25,
  'rgb_1_g': 23,
  'rgb_1_b': 24
}

LED_PINS = [
  'rgb_1_r', 'rgb_1_g', 'rgb_1_b'
]

PWM_PINS = {}

UDP_IP = "192.168.0.255"
UDP_PORT = 11647


# GPIO SETUP
# -------------------------------------
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

for pin in LED_PINS:
  pin_id = PINS[pin]

  GPIO.setup(pin_id, GPIO.OUT)
  GPIO.output(pin_id, GPIO.LOW)

  PWM_PINS[pin] = GPIO.PWM(pin_id, 50)
  PWM_PINS[pin].start(0)


# SOCKET SETUP
# -------------------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


# LISTEN
# -------------------------------------
hue = 0.0
brightness = 1.0
saturation = 1.0

while True:
  hue, addr = sock.recvfrom(4)
  
  color = colorsys.hsv_to_rgb(float(hue), saturation, brightness)
  PWM_PINS['rgb_1_r'].ChangeDutyCycle(int(color[0]*100.0))
  PWM_PINS['rgb_1_g'].ChangeDutyCycle(int(color[1]*100.0))
  PWM_PINS['rgb_1_b'].ChangeDutyCycle(int(color[2]*100.0))
