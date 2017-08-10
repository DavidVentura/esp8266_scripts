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


def get_ssids_and_qual():
    w = network.WLAN()
    ssids = w.scan()
    ret = []
    for item in ssids:
        ret.append((item[0].decode(), rssi_to_perc(item[3])))

    return sorted(ret, key=lambda tup: tup[1], reverse=True)


def rssi_to_perc(rssi):
    return min(max(2 * (rssi + 100), 0), 100)
