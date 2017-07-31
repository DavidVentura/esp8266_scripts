import usocket as socket
import dns
import time
s = None


def parse_req(req):
    # req = [ "GET /toggle HTTP/1.1", ....]
    req = req[0]
    if " " not in req:
        return None, None
    # r = "GET /toggle?asd=3&bbb=4 HTTP/1.1"
    r = req.split(" ")[1]
    # r = "/toggle?asd=3&bbb=4"
    path = r[1:]
    # path = "toggle?asd=3&bbb=4"
    tmp = path.split("?")
    endpoint = tmp[0]
    params = {}
    if len(tmp) > 1:
        s_params = tmp[1]
        # s_params = asd=3&bbb=4
        params = {}
        for param in s_params.split("&"):
            # param = 'asd=3' .. 'bbb=4'
            key, value = param.split('=')
            params[key] = value

    return endpoint, params


def debug(*msg):
    if True:
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

            path, params = parse_req(r)
            debug("PATH: ", path)
            debug("PARAMS: ", params)

            cl.send("HTTP/1.1 200 OK\r\n\r\n")
            cl.write(data)
            cl.close()
            if path == 'config':
                return 'right in the kokoro', 'tacotaco'
        except OSError:
            # timeouts
            pass
        except Exception as e:
            print(e)
        time.sleep_ms(100)
