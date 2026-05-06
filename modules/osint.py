#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import requests, socket, webbrowser, concurrent.futures, time
from core.display import get_inpt, menu_opts, Colors, Colorate, Theme
from modules.email_lookup import email_lookup_init

def _g(u):
    try:
        r = requests.get(u, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

def whois_lookup(v):
    cl = Theme.get_colors()
    ip = 0
    try: socket.inet_aton(v); ip = 1
    except: pass
    r = {}
    if ip:
        g, n = _g(f"http://ip-api.com/json/{v}?fields=66846719"), _g(f"https://rdap.org/ip/{v}")
        if g and g.get("status") == "success":
            for f in ["country","regionName","city","zip","lat","lon","timezone","isp","org","as","mobile","proxy","hosting"]:
                if g.get(f): r[f.upper()] = g[f]
        if n:
            r["NET_NAME"], r["NET_HANDLE"], r["CIDR"] = n.get("name","N/A"), n.get("handle","N/A"), n.get("parentHandle","N/A")
            for e in n.get("entities", []):
                if "abuse" in e.get("roles", []):
                    for v in e.get("vcardArray", [None, []])[1]:
                        if v[0] == "email": r["ABUSE_EMAIL"] = v[3]
    else:
        d = _g(f"https://rdap.org/domain/{v}")
        if not d: return {"ERR": "Domain not found"}
        r["DOMAIN"] = d.get("handle", v)
        for e in d.get("entities", []):
            rs = e.get("roles", [])
            if "registrar" in rs or "registrant" in rs:
                for vc in e.get("vcardArray", [None, []])[1]:
                    if vc[0] == "fn": r[f"{rs[0].upper()}_NAME"] = vc[3]
                    if vc[0] == "email": r[f"{rs[0].upper()}_MAIL"] = vc[3]
        for ev in d.get("events", []):
            a = ev.get("eventAction")
            if a in ["registration", "expiration", "last changed"]: r[a.replace(" ","_").upper()] = ev.get("eventDate")
    return r

def dns_lookup(t):
    try: return {"IP": socket.gethostbyname(t), "HOST": t}
    except: return {"error": "failed"}

def ip_pinger():
    cl = Theme.get_colors()
    h = get_inpt("host:")
    p = int(get_inpt("port (80):") or 80)
    b = int(get_inpt("bytes (64):") or 64)
    print(Colorate.Horizontal(cl["head"], f"\n  [+] Pinging {h}:{p}... (CTRL+C)\n"))
    def _png():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                st = time.time()
                s.connect((h, p))
                s.sendall(b'\x00' * b)
                ms = (time.time() - st) * 1000
                print(Colorate.Horizontal(cl["head"], f"  [+] Reply from {h}: {ms:.2f}ms"))
        except: print(Colorate.Horizontal(cl["num"], f"  [!] Timeout: {h}"))
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
            while 1: ex.submit(_png); time.sleep(0.1)
    except: print(Colorate.Horizontal(cl["num"], "\n  [!] Stopped."))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
