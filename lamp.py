import http
from machine import Pin

data = open("lamp.html").read()
pin2 = Pin(2, Pin.OUT)
value = 0


def set_pin(val):
    global value
    value = val
    pin2.value(val)


def on():
    set_pin(0)
    return data


def off():
    set_pin(1)
    return data


def toggle():
    val = (value + 1) % 2
    set_pin(val)
    return data


def get():
    return str(value)


set_pin(value)
http.serve({
    'on': on,
    'off': off,
    'toggle': toggle,
    'get': get
    })
