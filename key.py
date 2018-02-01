import mido 
import time
import math
import serial
from colorsys import hsv_to_rgb
from neopixel import *
from neopixel import Color as NeoColor
from chroma import Color

# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

def map_value(i, il, ih, ol, oh):
    return (i - il) / (ih - il) * (oh - ol) + ol

notes = []
leds = [Color("#000000") for x in range(LED_COUNT)]

ports = mido.get_input_names()
if len(ports) == 1:
    print("Warning: only one input port detected.")
    print("If {} looks like your device, all is well.".format(ports[0]))
else:
    print("{} ports detected, lazily using the first: {}".format(len(ports), ports[0]))

device_name = ports[0]

in_port = mido.open_input(ports[0])

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

def shift():
    for i in range(0, len(leds)-1):
        leds[len(leds)-1 - i] = leds[len(leds)-1 - i - 1]

def show_list():
    for i in range(len(leds)):
        color = leds[i]

        #  hsv = list(color.hsv)
        #  hsv[2] = 0.5 * (1 + math.sin(i / 20))
        #  color.hsv = tuple(hsv)

        color = NeoColor(*[round(x * 255) for x in color.rgb])
        strip.setPixelColor(i, color)
    strip.show()

switch_i = 0

def dim(c, b):
    hls = c.hls
    n = Color()
    n.hls = (hls[0], b / 2, hls[2])
    return n

while True:
    for message in in_port.iter_pending():
        if message.type == 'note_on':
            m_note = message.note
            if m_note not in notes:
                notes.append(m_note)
        elif message.type == 'note_off':
            m_note = message.note
            if m_note in notes:
                notes.remove(m_note)

    colors = []
    for led in leds:
        led = Color("#000000")

    for note in notes:
        leds[note + 20] = Color("#FFFFFF")
    show_list()
