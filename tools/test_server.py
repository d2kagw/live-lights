import RPi.GPIO as GPIO
import time
import colorsys
import socket


# CONSTANTS
# -------------------------------------
PINS = {
  'led_power_1': 17,

  'button_1': 12,
  'button_2': 5,
  'button_3': 6,

  'rgb_1_r': 16,
  'rgb_1_g': 21,
  'rgb_1_b': 20,

  'rgb_2_r': 26,
  'rgb_2_g': 13,
  'rgb_2_b': 19
}

PINS_LED = [
  'led_power_1',
  'rgb_1_r', 'rgb_1_g', 'rgb_1_b',
  'rgb_2_r', 'rgb_2_g', 'rgb_2_b'
]

PINS_RGB_LED = [
  'rgb_1_r', 'rgb_1_g', 'rgb_1_b',
  'rgb_2_r', 'rgb_2_g', 'rgb_2_b'
]

PWM_PINS = {}

PINS_SWITCH = [
  'button_1',
  'button_2',
  'button_3'
]

UDP_IP = "192.168.0.255"
UDP_PORT = 11647

FPS = 1.0/24.0


# GPIO SETUP
# -------------------------------------
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

for pin in PINS_LED:
  pin_id = PINS[pin]
  
  GPIO.setup(pin_id, GPIO.OUT)
  GPIO.output(pin_id, GPIO.LOW)

for pin in PINS_RGB_LED:
  pin_id = PINS[pin]
  
  PWM_PINS[pin] = GPIO.PWM(pin_id, 50)
  PWM_PINS[pin].start(0)

for pin in PINS_SWITCH:
  pin_id = PINS[pin]
  
  GPIO.setup(pin_id, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(PINS['led_power_1'], GPIO.HIGH)


# BUTTON SETUP
# -------------------------------------
def button_1_callback(channel):
  print "button 1"

def button_2_callback(channel):
  print "button 2"

def button_3_callback(channel):
  print "button 3"

GPIO.add_event_detect(PINS['button_1'], GPIO.FALLING, callback=button_1_callback, bouncetime=300)
GPIO.add_event_detect(PINS['button_2'], GPIO.FALLING, callback=button_2_callback, bouncetime=300)
GPIO.add_event_detect(PINS['button_3'], GPIO.FALLING, callback=button_3_callback, bouncetime=300)


# SOCKET SETUP
# -------------------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


# BROADCAST
# -------------------------------------
hue = [ 0.0, 0.5 ]

while True:
  sock.sendto("%0.2f" % (hue[0]), (UDP_IP, UDP_PORT))
  
  print "hue %0.2f - %0.2f" % (hue[0], hue[1])

  color = colorsys.hsv_to_rgb(hue[0], 1.0, 1.0)
  PWM_PINS['rgb_1_r'].ChangeDutyCycle(int(color[0]*100))
  PWM_PINS['rgb_1_g'].ChangeDutyCycle(int(color[1]*100))
  PWM_PINS['rgb_1_b'].ChangeDutyCycle(int(color[2]*100))

  hue[0] = 0.0 if hue[0] > 1.0 else (hue[0] + 0.01)
  
  color = colorsys.hsv_to_rgb(hue[1], 1.0, 1.0)
  PWM_PINS['rgb_2_r'].ChangeDutyCycle(int(color[0]*100))
  PWM_PINS['rgb_2_g'].ChangeDutyCycle(int(color[1]*100))
  PWM_PINS['rgb_2_b'].ChangeDutyCycle(int(color[2]*100))

  hue[1] = 0.0 if hue[1] > 1.0 else (hue[1] + 0.01)

  time.sleep(FPS)
