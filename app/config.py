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
    rpi.SwitchPin('toggle', 12),
    rpi.SwitchPin('adjust_1', 5),
    rpi.SwitchPin('adjust_2', 6)
  ]

  RPI_POWER_LED = rpi.LEDPin('power', 17)

  RPI_RGB_LEDS = [
    [
      rpi.LEDPin('rgb_1_r', 16, True),
      rpi.LEDPin('rgb_1_g', 21, True),
      rpi.LEDPin('rgb_1_b', 20, True)
    ],
    [
      rpi.LEDPin('rgb_2_r', 26, True),
      rpi.LEDPin('rgb_2_g', 13, True),
      rpi.LEDPin('rgb_2_b', 19, True)
    ]
  ]

# ------------------------------

UDP_IP = "192.168.0.255"
UDP_PORT = 11647

# ------------------------------

FPS = 1.0 / 12.0

VIDEO_RATIO  = 16.0 / 9.0
VIDEO_WIDTH  = 1920 / 6
VIDEO_HEIGHT = int(math.ceil( VIDEO_WIDTH / VIDEO_RATIO ))

STRIP_COLUMNS = 18 # includes corners/edges
STRIP_ROWS    = 10 # includes corners/edges
STRIP_TOTAL   = ( ( STRIP_COLUMNS + STRIP_ROWS ) * 2 ) - 4

# LED_TV_LED_WIDTH    = ceil( VIDEO_WIDTH / ( LED_TV_COLUMNS * 1.0 ) )
# LED_TV_LED_HEIGHT   = ceil( ceil( VIDEO_WIDTH / VIDEO_RATIO ) / LED_TV_ROWS )
# LED_TV_LED_COVERAGE = 100

# DISPLAY_WIDTH  = VIDEO_WIDTH
# DISPLAY_HEIGHT = VIDEO_HEIGHT
