import mido 
import serial

from colorsys import hsv_to_rgb
from chroma import Color

def map_value(i, il, ih, ol, oh):
    return (i - il) / (ih - il) * (oh - ol) + ol


notes = []

ports = mido.get_input_names()
if len(ports) == 1:
    print("Warning: only one input port detected.")
    print("If {} looks like your device, all is well.".format(ports[0]))
else:
    print("{} ports detected, lazily using the first: {}".format(len(ports), ports[0]))

device_name = ports[0]

in_port = mido.open_input(ports[0])

while True:
    message = in_port.receive()
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
