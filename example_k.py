import http
import machine, neopixel
from ktorgb import ktorgb
import time


def kset(k, i):
    set_all(neo, ktorgb(int(k)), float(i))
    return ""


def set_all(np, ratio, intensity):
    color = tuple(int(intensity * k) for k in ratio)
    for i in range(np.n):
        np[i] = color
        np.write()
        time.sleep_ms(40)


def setup():
    return neopixel.NeoPixel(machine.Pin(2), 8)


neo = setup()
http.serve({'ktorgb': kset})
