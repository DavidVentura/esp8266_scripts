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


def config(ssid, password):
    ssid = ssid.replace('+', ' ')
    print("Data provided:", ssid, password)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Resetting!")
    wait_until_connected(wlan)
    time.sleep(2)
    print("Resetting!")
    machine.reset()


def list_ssids():
    ret = []
    for item in get_ssids_and_qual():
        ret.append('''<p>
                        <label>
                            <input type="radio" name="ssid" value="%s">
                            <b>%s</b> <small>%d%%</small>
                        </label>
                      </p>\n''' % (item[0], item[0], item[1]))
    data = ''.join(ret)
    s = open('ssidlist.html').read().replace('{{list}}', data)
    return s


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('connecting to network...')
    conn = wait_until_connected(wlan)

    TESTING = True
    if not conn or TESTING:
        setup_ap()
        import http
        http.serve({'': list_ssids,
                    'config': config})

    else:
        disable_ap()
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


def setup_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="Test_SSID_Please_config", authmode=1)
    print("AP set up")


def disable_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
