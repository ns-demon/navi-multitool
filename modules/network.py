#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import socket, threading, requests, os
from core.display import Colors, Colorate, get_inpt, Theme

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

def clone_website(url):
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], f"  [+] Cloning {url}..."))
    try:
        if not url.startswith("http"): url = "https://" + url
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            name = url.split("//")[-1].replace("/", "_") + ".html"
            if not os.path.exists("output"): os.makedirs("output")
            with open(f"output/{name}", "w", encoding="utf-8") as f:
                f.write(r.text)
            print(Colorate.Horizontal(cl["head"], f"  [>] Success! Saved to output/{name}"))
        else:
            print(Colorate.Horizontal(cl["num"], f"  [!] Failed with status {r.status_code}"))
    except Exception as e:
        print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
    input("\n  Press Enter...")
