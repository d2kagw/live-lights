#!/usr/bin/env python
import sys, logging
import math

VIDEO_RATIO  = 16.0 / 9.0
VIDEO_WIDTH  = 1920 / 6
VIDEO_HEIGHT = math.ceil( VIDEO_WIDTH / VIDEO_RATIO )

# LED Constants
LED_TV_COLUMNS = 18
LED_TV_ROWS    = 10
LED_TV_TOTAL   = ( ( LED_TV_COLUMNS + LED_TV_ROWS ) * 2 ) - 4

LED_TV_LED_WIDTH    = math.ceil( VIDEO_WIDTH / ( LED_TV_COLUMNS * 1.0 ) )
LED_TV_LED_HEIGHT   = math.ceil( math.ceil( VIDEO_WIDTH / VIDEO_RATIO ) / LED_TV_ROWS )
LED_TV_LED_COVERAGE = 100 # PERCENT

LED_SURROUND_MAX      = 4 # Don't change this
LED_SURROUND_COUNT    = 2 # 0 = no surround lights, currently 4 max...
LED_SURROUND_COVERAGE = 25 # PERCENT

# Display Constants
DISPLAY_WIDTH  = VIDEO_WIDTH
DISPLAY_HEIGHT = VIDEO_HEIGHT
COLOR_SPACE    = 255

def main(prog_args):
  setup()
  logging.debug('hit')
  print "done %f.2", (VIDEO_HEIGHT)

def setup():
  # Logging
  logging.basicConfig(level=logging.DEBUG, filename='server.log')  
    
if __name__ == "__main__":
  sys.exit(main(sys.argv))
