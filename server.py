import mido 
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
    for i in range(1, len(leds)):
        leds[len(leds) - i] = leds[len(leds) - i + 1]

def show_list():
    mid = strip.numPixels() / 2
    for i in range(mid):
        strip.setPixelColor(mid - i, leds[i])
        strip.setPixelColor(mid + i, leds[i])
    strip.show()

while True:
    shift()
    for message in in_port.iter_pending():
        m_note, m_type = message.note, message.type
        if m_type == 'note_on':
            notes.append(m_note)
        else:
            notes.remove(m_note)

    colors = []
    for note in notes:
        color_value = map_value(note, 21, 108, 0, 1)
        colors.append(Color(hsv_to_rgb(color_value, 1, 1), 'RGB'))

    if colors:
        #  new = colors[0]
        #  for color in colors[1:]:
            #  new = new + color
        #  color = new
        color = colors[-1]
    else:
        color = Color('#000000')

    rgb = [round(x * 127) for x in color.rgb]
    print(rgb)
