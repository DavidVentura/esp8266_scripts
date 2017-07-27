import http
import machine, neopixel
from ktorgb import ktorgb
import time


def kset(k, i, count=8):
    set_all(neo, ktorgb(int(k)), float(i), int(count))
    return ""


def set_all(np, ratio, intensity, count):
    count = max(min(count, np.n), 1)
    color = tuple(int(intensity * k) for k in ratio)

    for i in range(count):
        np[i] = color
        np.write()
        time.sleep_ms(40)

    for i in range(count, np.n):
        np[i] = (0, 0, 0)
        np.write()
        time.sleep_ms(40)


def setup():
    return neopixel.NeoPixel(machine.Pin(2), 8)


neo = setup()
http.serve({'ktorgb': kset})
