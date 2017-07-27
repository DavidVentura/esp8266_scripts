import usocket as socket


def debug(*msg):
    if False:
        print(*msg)


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


def serve(cbmap):
    """
    cbmap: dictionary of functions where the key is the path
    with the leading '/' stripped
    """
    # size of the chunks to transmit
    n = 1000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    debug("about to listen")
    s.listen(1)

    while True:
        debug('waiting...')
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

        if path not in cbmap:
            debug("notincbmap")
            cl.send("HTTP/1.1 400 Invalid Request\r\n\r\n")
            cl.close()
            continue

        try:
            data = cbmap[path](**params)
            if data is None:
                data = ""
            cl.send("HTTP/1.1 200 OK\r\n\r\n")
            html = [data[i:i+n] for i in range(0, len(data), n)]
            for h in html:
                cl.send(h)
        except Exception as e:
            cl.send("HTTP/1.1 500 Internal Server Error\r\n\r\n")
            cl.send(str(e))
        finally:
            cl.close()
            debug('conn closed')
