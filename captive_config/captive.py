import time
import network
import machine


def wait_until_connected(wlan):
    count = 0
    while not wlan.isconnected() and count < 10:
        print("Waiting...")
        time.sleep(1)
        count += 1

    return wlan.isconnected()


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('connecting to network...')
    conn = wait_until_connected(wlan)

    if not conn:
        import http
        ssid, password = http.serve('hey pls config me')
        print("Data provided:", ssid, password)
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)

        print("Resetting!")
        wait_until_connected(wlan)
        time.sleep(2)
        print("Resetting!")
        machine.reset()

    else:
        print('network config:', wlan.ifconfig())
