#!/usr/bin/env python
import math
import rpi

RPI_SWITCHES = []
RPI_POWER_LED = False
RPI_RGB_LEDS = []

def setup_rpi():
  global RPI_SWITCHES
  global RPI_POWER_LED
  global RPI_RGB_LEDS

  RPI_SWITCHES = [
    rpi.SwitchPin('toggle_analysis_schema', 12),
    rpi.SwitchPin('toggle_analysis_mode', 5),
    rpi.SwitchPin('toggle_image_mode', 6),
    rpi.SwitchPin('adjust_image_mode', 25)
  ]

  RPI_POWER_LED = rpi.LEDPin('power', 17)

  RPI_RGB_LEDS = [
    rpi.RGBPin('RGB_a', 16, 21, 20),
    rpi.RGBPin('RGB_b', 26, 13, 19)
  ]

# ------------------------------

UDP_IP = "192.168.0.255"
UDP_PORT = 11647

# ------------------------------

FPS = 1.0 / 24.0

OUTPUT_STRIP = True
OUTPUT_SURROUND = True
OUTPUT_WINDOW = True

VIDEO_RATIO  = 16.0 / 9.0
VIDEO_WIDTH  = 1920 / 6
VIDEO_HEIGHT = int(math.ceil( VIDEO_WIDTH / VIDEO_RATIO ))

STRIP_COLUMNS = 18 # includes corners/edges
STRIP_ROWS    = 10 # includes corners/edges
STRIP_TOTAL   = ( ( STRIP_COLUMNS + STRIP_ROWS ) * 2 ) - 4

ANALYSIS_COVERAGE = 0.3 # 0.9 = ~10%, 0.1 = ~90%
