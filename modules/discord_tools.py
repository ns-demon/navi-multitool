import time, urllib.request, urllib.error, urllib.parse, json, requests, random, string, threading, webbrowser
from datetime import datetime, timezone
from core.display import Colors, Colorate, get_inpt, Theme

def _snd(url, d, m='POST'):
    try:
        _d = json.dumps(d).encode('utf-8') if d else b''
        r = urllib.request.Request(url, data=(_d if m=='POST' else None), method=m)
        r.add_header('User-Agent', 'Navi_Wired/1.0')
        r.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(r) as rs: return rs.status
    except: return -1

def webhook_spam(url, msg, amt=10):
    cl = Theme.get_colors()
    print("\n  [+] Initializing spam...") 
    sc, p = 0, {"content": msg, "username": "Navi@WIRED", "avatar_url": "https://i.ibb.co/Wv94YGVx/navi.png"} # yes hardcoded username & pfp. deal with it.
    for i in range(amt):
        st = _snd(url, p)
        if st in [200, 204]:
            print(Colorate.Horizontal(cl["head"], f"  [>] Sent {i+1}/{amt}"))
            sc += 1
        else: print(Colorate.Horizontal(cl["num"], f"  [!] Failed {i+1}"))
        time.sleep(0.15) 
    print(Colorate.Horizontal(cl["head"], f"\n  [=] Done: {sc} hits."))
    input("  Press enter...")

def webhook_delete(url):
    cl = Theme.get_colors()
    print("\n  [+] Deleting hook...")
    res = _snd(url, {}, m='DELETE')
    if res in [200, 204]: print(Colorate.Horizontal(cl["head"], "  [>] Erased."))
    else: print(Colorate.Horizontal(cl["num"], "  [!] Error deleting."))
    input("  Press enter...")

def id_to_token(uid):
    import base64
    try: return base64.b64encode(str(uid).encode()).decode()
    except: return "???"

def pfp_lookup(uid):
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], "  [+] Fetching pfp..."))
    try:
        r = requests.get(f"https://dcdn.dstn.to/profile/{uid}")
        if r.status_code == 200:
            d = r.json()
            if "user" in d and d["user"]["avatar"]:
                h = d["user"]["avatar"]
                e = "gif" if h.startswith("a_") else "png"
                print(Colorate.Horizontal(cl["head"], f"  [>] URL: https://cdn.discordapp.com/avatars/{uid}/{h}.{e}?size=1024"))
            else: print(Colorate.Horizontal(cl["num"], "  [!] No avatar."))
        else: print(Colorate.Horizontal(cl["num"], "  [!] Not found."))
    except: print(Colorate.Horizontal(cl["num"], "  [!] Request failed."))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def banner_lookup(uid):
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], "  [+] Fetching banner..."))
    try:
        r = requests.get(f"https://dcdn.dstn.to/profile/{uid}")
        if r.status_code == 200:
            d = r.json()
            if "user" in d and d["user"]["banner"]:
                h = d["user"]["banner"]
                e = "gif" if h.startswith("a_") else "png"
                print(Colorate.Horizontal(cl["head"], f"  [>] URL: https://cdn.discordapp.com/banners/{uid}/{h}.{e}?size=1024"))
            else: print(Colorate.Horizontal(cl["num"], "  [!] No banner."))
        else: print(Colorate.Horizontal(cl["num"], "  [!] Not found."))
    except: print(Colorate.Horizontal(cl["num"], "  [!] Request failed."))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def server_info_lookup(inv):
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], "  [+] Fetching server..."))
    try:
        c = inv.split("/")[-1] if "/" in inv else inv
        r = requests.get(f"https://discord.com/api/v9/invites/{c}")
        if r.status_code == 200:
            d = r.json()
            g = d.get("guild", {})
            print(Colorate.Horizontal(cl["num"], "  [=] Name: ") + Colorate.Horizontal(cl["txt"], str(g.get("name"))))
            print(Colorate.Horizontal(cl["num"], "  [=] ID: ") + Colorate.Horizontal(cl["txt"], str(g.get("id"))))
            if "inviter" in d:
                i = d["inviter"]
                print(Colorate.Horizontal(cl["num"], "  [=] Inviter: ") + Colorate.Horizontal(cl["txt"], f"{i.get('username')} ({i.get('id')})"))
        else: print(Colorate.Horizontal(cl["num"], "  [!] Invalid invite."))
    except: print(Colorate.Horizontal(cl["num"], "  [!] Error."))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def nitro_generator(tc=1):
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], f"  [+] Nitro Gen starting ({tc} threads)..."))
    def _chk():
        while True:
            c = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
            try:
                r = requests.get(f"https://discordapp.com/api/v9/entitlements/gift-codes/{c}?with_application=false&with_subscription_plan=true", timeout=3)
                if r.status_code == 200:
                    print(Colorate.Horizontal(cl["head"], f"\n  [$$$] VALID: discord.gift/{c}"))
                    with open("hits.txt", "a") as f: f.write(f"discord.gift/{c}\n")
                else: print(Colorate.Horizontal(cl["num"], f"  [!] Invalid: {c}"))
            except: pass
            time.sleep(0.05)
    try:
        for _ in range(tc): threading.Thread(target=_chk, daemon=True).start()
        while True: time.sleep(1)
    except: print(Colorate.Horizontal(cl["head"], "\n  [=] Stopped."))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def bot_invite_gen(bid):
    cl = Theme.get_colors()
    l = f"https://discord.com/oauth2/authorize?client_id={bid}&scope=bot&permissions=8"
    print(Colorate.Horizontal(cl["head"], f"  [>] Link: {l}"))
    if input(Colorate.Horizontal(cl["num"], "  Open? (y/n): ")).lower() == 'y':
        try: webbrowser.open(l)
        except: pass
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def token_info(tk):
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], "  [+] Fetching account..."))
    h = {"Authorization": tk, "Content-Type": "application/json"}
    try:
        r = requests.get("https://discord.com/api/v9/users/@me", headers=h)
        if r.status_code != 200:
            print(Colorate.Horizontal(cl["num"], "  [!] Invalid Token."))
            return
        j = r.json()
        id, un = j.get("id"), f"{j.get('username')}#{j.get('discriminator')}"
        nit = {1:"Classic",2:"Boost",3:"Basic"}.get(j.get("premium_type", 0), "None")
        ts = ((int(id) >> 22) + 1420070400000) / 1000
        cr = datetime.fromtimestamp(ts, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        gs = "N/A"
        try: gs = str(len(requests.get("https://discord.com/api/v9/users/@me/guilds", headers=h).json()))
        except: pass
        ln = "  " + "─" * 50
        print(Colorate.Horizontal(cl["head"], ln))
        for k, v in [("User",un),("ID",id),("Email",j.get("email","N/A")),("Nitro",nit),("Created",cr),("Guilds",gs)]:
            print(Colorate.Horizontal(cl["num"], f"  [>] {k:<10}: ") + Colorate.Horizontal(cl["txt"], str(v)))
        print(Colorate.Horizontal(cl["main"], ln))
    except: print(Colorate.Horizontal(cl["num"], "  [!] Failed."))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
