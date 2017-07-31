import usocket as socket
import dns
import time
s = None


def debug(*msg):
    if False:
        print(*msg)


def serve(data):
    global s
    dns.setup_dns()
    if s is None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 80))
        debug("about to listen")
        s.listen(1)
        s.settimeout(2)

    while 1:
        debug('waiting...')
        dns.serve()
        try:
            cl, addr = s.accept()
            debug('client connected from', addr)
            request = cl.recv(1024)
            r = str(request, 'utf-8').split('\r\n')

            debug("*" * 20, "Request", "*" * 20)
            debug(r)
            debug("*" * 20, "Request", "*" * 20)

            cl.send("HTTP/1.1 200 OK\r\n\r\n")
            cl.write(data)
            cl.close()
        except OSError:
            # timeouts
            pass
        except Exception as e:
            print(e)
        time.sleep_ms(100)
