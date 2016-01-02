#!/usr/bin/env python
import sys, signal
import logging, math, time

import config

import rpi
rpi.setup()
config.setup_rpi()

import manager

# ------------------------------

def cleanup(): 
  print "Shutting down..."
  rpi.cleanup()
  mngr.cleanup()

def exit_handler(signum, frame):
  cleanup()
  sys.exit()

signal.signal(signal.SIGINT, exit_handler)

# ------------------------------

mngr = manager.Manager()

# toggle_analysis_schema
config.RPI_SWITCHES[0].click( mngr.toggle_analysis_schema )

# toggle_analysis_mode
config.RPI_SWITCHES[1].click( mngr.toggle_analysis_mode )

# toggle_image_mode
config.RPI_SWITCHES[2].click( mngr.toggle_image_mode )

# adjust_image_mode
config.RPI_SWITCHES[3].click( mngr.adjust_image_mode )

# ------------------------------

config.RPI_POWER_LED.on()

# ------------------------------

while True:
  mngr.go()

cleanup()
