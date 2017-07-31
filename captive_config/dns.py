import socket
import network

# based on
# https://github.com/amora-labs/micropython-captive-portal/blob/master/captive.py


def parse_dgram(data):
    print("Reading datagram data...")
    m = data[2]
    tipo = (m >> 3) & 15   # Opcode bits
    dominio = ''
    if tipo == 0:                     # Standard query
        ini = 12
        lon = data[ini]
        while lon != 0:
            dominio += data[ini+1:ini+lon+1].decode("utf-8") + '.'
            ini += lon + 1
            lon = data[ini]
    return dominio


def respuesta(data, ip):
    packet = b''
    dominio = parse_dgram(data)
    print("Resposta {} == {}".format(dominio, ip))
    if dominio:
        packet += data[:2] + b"\x81\x80"
        # Questions and Answers Counts
        packet += data[4:6] + data[4:6] + b'\x00\x00\x00\x00'
        # Original Domain Name Question
        packet += data[12:]
        # Pointer to domain name
        packet += b'\xc0\x0c'
        # Response type, ttl and resource data length -> 4 bytes
        packet += b'\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'

        packet += bytes(map(int, ip.split('.')))
        # 4 bytes of IP
    return dominio, packet


def setup_dns():
    global udps
    global ip
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="Change my LED", authmode=1)

    ip = ap.ifconfig()[0]
    print(ap.ifconfig())
    if ip == '0.0.0.0':
        ip = '192.168.4.1'

    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # udps.setblocking(False)
    udps.setblocking(False)
    udps.bind(('', 53))


def serve():
    global udps
    try:
        data, addr = udps.recvfrom(1024)
        print("incoming datagram...")
        dom, answer = respuesta(data, ip)
        udps.sendto(answer, addr)
        print('Replying: {:s} -> {:s}'.format(dom, ip))
    except Exception as e:
        pass
        # print("No dgram")
