import time
import network
import machine


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        count = 0
        while not wlan.isconnected() and count < 10:
            print("Waiting...")
            time.sleep(1)
            count += 1

    if not wlan.isconnected():
        import http
        ssid, password = http.serve('hey pls config me')
        wlan.connect(ssid, password)
        print("Resetting!")
        time.sleep(2)
        print("Resetting!")
        machine.reset()

    else:
        print('network config:', wlan.ifconfig())
