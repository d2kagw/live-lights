#!/usr/bin/env python
import sys, signal
import logging, math, time

import config

import rpi
rpi.setup()
config.setup_rpi()

import strip
import manager

# ------------------------------

def cleanup(): 
  print "Shutting down..."
  rpi.cleanup()

def exit_handler(signum, frame):
  cleanup()
  sys.exit()

signal.signal(signal.SIGINT, exit_handler)

# ------------------------------

mngr = manager.Manager()
config.RPI_SWITCHES[0].click( mngr.toggle )
config.RPI_SWITCHES[1].click( mngr.adjust_a )
config.RPI_SWITCHES[2].click( mngr.adjust_b )

# ------------------------------

power_led = config.RPI_POWER_LED.on()

# ------------------------------

while True:
  mngr.go()
  time.sleep(config.FPS)

cleanup()
