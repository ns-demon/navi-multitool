import socket, threading

def _hp(ip, p, r, i):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        if s.connect_ex((ip, p)) == 0: r[i] = p
        s.close()
    except: pass

def do_port_check(ip):
    o, ts = [None] * 1025, []
    for x in range(1, 1025):
        t = threading.Thread(target=_hp, args=(ip, x, o, x))
        ts.append(t); t.start()
    [t.join() for t in ts]
    return [x for x in o if x is not None]
