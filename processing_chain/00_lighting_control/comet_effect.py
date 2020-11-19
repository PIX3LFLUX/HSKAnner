#!/usr/bin/env python

from time import sleep
from sys import argv
import board
import neopixel

# LED strip configuration:
LED_COUNT   = int(argv[1])      # Number of LED pixels.
tail_len = int(argv[2]) # the tail will consist of tail_len-1 leds, with one led leading with 100% of what was set for the rgb values.
LED_PIN     = board.D18      # GPIO pin
LED_BRIGHTNESS = float(argv[3])  # LED brightness
LED_ORDER = neopixel.GRBW # order of LED colours. May be GRB, RGB, GRBW, or RGBW
# effect config
comet_r = int(argv[4])
comet_g = int(argv[5])
comet_b = int(argv[6])
comet_w = int(argv[7])
sleeptime = float(argv[8])    # change this value to adjust the speed of the effect. 0 is no wait in between cycles.


# Create NeoPixel object with appropriate configuration.
strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness = LED_BRIGHTNESS, auto_write=False, pixel_order = LED_ORDER)

# effect
strip.fill((0,0,0,0))

def comet_init(tail_len):
    for jj in range(tail_len):
        cc = (tail_len - jj) / (tail_len * (jj + 1))  # brightness factor for tail. Since brightness does not scale linearly, i chose (n-x)/(n*(x+1)) for scaling, where n is the tail length and x is the distance from the brightest LED.
        strip[jj % LED_COUNT] = (int(comet_r*cc),int(comet_g*cc),int(comet_b*cc),int(comet_w*cc))

def comet_loop():
    global strip
    buf = strip[0]
    strip[0:LED_COUNT-1] = strip[1:LED_COUNT]   # weird python adressing. why not ([0:LED_COUNT-2] and [1:LED_COUNT-1]?)
    strip[LED_COUNT-1] = buf
    strip.show()

try:
    comet_init(tail_len)
    while True:
        comet_loop()
        sleep(sleeptime)        
finally:
    strip.fill((0,0,0,0))
    strip.show()
