#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import sys, time, subprocess, json, os, threading, zipfile, io, shutil

def _init():
    try: import pystyle, requests, selenium, dns.resolver, bs4, socks, websocket, piexif, exifread, mutagen, PyQt5
    except: subprocess.check_call([sys.executable, "-m", "pip", "install", "pystyle", "requests", "selenium", "dnspython", "beautifulsoup4", "pysocks", "websocket-client", "piexif", "exifread", "mutagen", "PyQt5", "-q"])


_init()

from core.display import Colors, Colorate, System, boot_anim, print_banner, menu_opts, get_inpt, init_os, get_config, Theme, matrix_effect
from modules.discord_tools import webhook_spam, webhook_delete, id_to_token, server_info_lookup, nitro_generator, bot_invite_gen
from modules.network import do_port_check
from modules.crypto import CryptXer, make_pw
from modules.sysinfo import get_sys_data
from modules.osint import whois_lookup, dns_lookup
from modules.malicious import mail_bomb
from modules.obfuscator import obfuscator_init
from modules.metadata import metadata_init

def cfg_mgr():
    while 1:
        _cl = Theme.get_colors()
        print_banner()
        print(Colorate.Horizontal(_cl["head"], "  [ CONFIGURATION & SETTINGS ]\n"))
        _tl = [("1","Blue"),("2","Red"),("3","Purple"),("4","Green"),("5","Yellow"),("6","Pink"),("7","Cyan"),("8","Gray"),("9","Rainbow"),("10","Modern"),("11","Modern Red"),("12","Modern Purple")]
        print(Colorate.Horizontal(_cl["head"], "  [ THEMES ]"))
        for _i in range(0, len(_tl), 3):
            _ln = ""
            for _k, _v in _tl[_i:_i+3]: _ln += Colorate.Horizontal(_cl["num"], f"  [{_k}] ") + Colorate.Horizontal(_cl["txt"], f"{_v:<15}")
            print(_ln)
        print("\n" + Colorate.Horizontal(_cl["head"], "  [ TOGGLES ]"))
        print(Colorate.Horizontal(_cl["num"], "  [13] ") + Colorate.Horizontal(_cl["txt"], "Auto-Update") + " " * 10 + Colorate.Horizontal(_cl["num"], "[14] ") + Colorate.Horizontal(_cl["txt"], "Discord Popup"))
        print(Colorate.Horizontal(_cl["num"], "  [99] ") + Colorate.Horizontal(_cl["txt"], "Return to Menu"))
        _c = get_inpt("navi@config:~#")
        if _c in [str(_x) for _x in range(1, 13)]:
            _tm = {"1":"blue","2":"red","3":"purple","4":"green","5":"yellow","6":"pink","7":"cyan","8":"gray","9":"rainbow","10":"modern","11":"modern_red","12":"modern_purple"}[_c]
            try:
                with open("core/config.json", "r") as _f: _d = json.load(_f)
                _d["theme"] = _tm
                with open("core/config.json", "w") as _f: json.dump(_d, _f, indent=2)
                print(Colorate.Horizontal(_cl["head"], f"  [+] Theme -> {_tm.upper()}"))
                matrix_effect(1, Theme.get_matrix_color())
            except: pass
        elif _c in ["13", "14"]:
            try:
                with open("core/config.json", "r") as _f: _d = json.load(_f)
                _k = "auto_update" if _c == "13" else "auto_open_discord"
                _d[_k] = not _d.get(_k, 1)
                with open("core/config.json", "w") as _f: json.dump(_d, _f, indent=2)
                print(Colorate.Horizontal(_cl["head"], f"  [+] {_k} is now {_d[_k]}"))
                time.sleep(1)
            except: pass
        elif _c == "99": break

def inf_view():
    _cl = Theme.get_colors()
    print_banner()
    try:
        with open("core/config.json", "r") as _f: _d = json.load(_f)
        for _k, _v in _d.items(): print(Colorate.Horizontal(_cl["num"], f"  {_k}: ") + Colorate.Horizontal(_cl["txt"], str(_v)))
    except: pass
    input(Colorate.Horizontal(_cl["head"], "\n  Press Enter..."))

def _pre():
    _cl, _cfg = Theme.get_colors(), get_config()
    if _cfg.get("auto_update"):
        try:
            import requests
            _r = requests.get("https://raw.githubusercontent.com/glockinhand/navi-multitool/main/core/config.json", timeout=5)
            if _r.status_code == 200:
                _rv = _r.json().get("version", "1.0.0")
                if _rv != _cfg.get("version"):
                    print(Colorate.Horizontal(_cl["num"], f"\n  [!] New Version Detected: {_rv}"))
                    _url = "https://github.com/glockinhand/navi-multitool/archive/refs/heads/main.zip"
                    _res = requests.get(_url, stream=True)
                    _dl, _ts = 0, int(_res.headers.get('content-length', 500000))
                    _io = io.BytesIO()
                    for _chunk in _res.iter_content(chunk_size=1024):
                        _dl += len(_chunk)
                        _io.write(_chunk)
                        _perc = int(30 * _dl / _ts)
                        if _perc > 30: _perc = 30
                        print(f"\r  {Colorate.Horizontal(_cl['num'], '[')}{Colorate.Horizontal(_cl['head'], '#' * _perc)}{Colorate.Horizontal(_cl['txt'], '-' * (30 - _perc))}{Colorate.Horizontal(_cl['num'], ']')} Downloading...", end="")
                    print("\n  " + Colorate.Horizontal(_cl["head"], "[+] Extracting update..."))
                    with zipfile.ZipFile(_io) as _zf:
                        _root = _zf.namelist()[0]
                        for _item in _zf.namelist():
                            if _item == _root: continue
                            _path = os.path.join(os.getcwd(), os.path.relpath(_item, _root))
                            if _item.endswith('/'):
                                if not os.path.exists(_path): os.makedirs(_path)
                            else:
                                with open(_path, "wb") as _f: _f.write(_zf.read(_item))
                    print(Colorate.Horizontal(_cl["head"], "  [+] Update installed! Rebooting Navi..."))
                    time.sleep(1.5)
                    os.execl(sys.executable, sys.executable, *sys.argv)
        except: pass

def _pop():
    _cfg = get_config()
    if _cfg.get("auto_open_discord"): # can be disabled in cfg 
        time.sleep(3)
        try:
            import webbrowser
            webbrowser.open(_cfg.get("discord", ""))
        except: pass

def _nbot_ui():
    _cl = Theme.get_colors()
    import base64
    
    token = ""
    config_path = "core/botcfg.json"
    
    default_config = {
        "BOT_TOKEN": "",
        "MESSAGE_CONTENT": "@everyone | Server Nuked | discord.gg/4qUD63pnPy | https://github.com/glockinhand/navi-multitool",
        "WEBHOOK_URL": "This webhook for tracking your nukes",
        "GUILD_NEW_NAME": "navi owns this",
        "CHANNEL_AMOUNT": 60,
        "BATCH_SIZE_CHANNELS": 60,
        "BATCH_SIZE_DELETE": 30,
        "BATCH_SIZE_BAN": 4,
        "TOTAL_MESSAGES": 800,
        "MAX_MESSAGES_PER_CHANNEL": 18,
        "TOTAL_WEBHOOKS": 2000,
        "WEBHOOK_DELAY": 0.06,
        "SPAM_EMOJIS": ["🏴", "🌙", "🔥", "💀", "👾"],
        "WEBHOOK_USERNAME": "Navi Runs Cord",
        "COMMAND_PREFIX": "."
    }
    
    if not os.path.exists("core"):
        os.makedirs("core")
        
    cfg_data = default_config.copy()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
                if isinstance(loaded_data, dict):
                    cfg_data.update(loaded_data)
                    token = cfg_data.get("BOT_TOKEN", "").strip()
        except Exception:
            pass
            
    if not token:
        print_banner()
        print(Colorate.Horizontal(_cl["head"], "  [ NUKE BOT ]\n"))
        print(Colorate.Horizontal(_cl["num"], "  Please enter Discord Bot Token:"))
        token = get_inpt("  Token: ").strip()
        if not token:
            print(Colorate.Horizontal(_cl["num"], "  [!] Token cannot be empty!"))
            time.sleep(1.5)
            return
            
        cfg_data["BOT_TOKEN"] = token
        
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(cfg_data, f, indent=2)
            print(Colorate.Horizontal(_cl["head"], "  [+] Token saved to core/botcfg.json!"))
            time.sleep(1)
        except Exception as e:
            print(Colorate.Horizontal(_cl["num"], f"  [!] Could not save token: {e}"))
            time.sleep(1.5)
            
    bot_id = "Unknown"
    try:
        parts = token.split('.')
        if len(parts) >= 1:
            padded = parts[0] + '=' * (4 - len(parts[0]) % 4)
            bot_id = base64.b64decode(padded).decode('utf-8')
    except Exception:
        pass
        
    bot_invite = f"https://discord.com/oauth2/authorize?client_id={bot_id}&scope=bot&permissions=8" if bot_id != "Unknown" else "Could not determine Bot ID"
    
    while True:
        print_banner()
        print(Colorate.Horizontal(_cl["head"], "  [ DISCORD NUKE BOT UI ]\n"))
        print(Colorate.Horizontal(_cl["num"], "  [=] Bot ID:     ") + Colorate.Horizontal(_cl["txt"], bot_id))
        print(Colorate.Horizontal(_cl["num"], "  [=] Bot Invite: ") + Colorate.Horizontal(_cl["head"], bot_invite))
        print("\n" + Colorate.Horizontal(_cl["head"], "  [ CONTROL PANEL ]"))
        print(Colorate.Horizontal(_cl["num"], "  [1] ") + Colorate.Horizontal(_cl["txt"], "Start Bot (New Window)"))
        print(Colorate.Horizontal(_cl["num"], "  [2] ") + Colorate.Horizontal(_cl["txt"], "Open botcfg.json"))
        print(Colorate.Horizontal(_cl["num"], "  [3] ") + Colorate.Horizontal(_cl["txt"], "Show Help"))
        print(Colorate.Horizontal(_cl["num"], "  [99]") + Colorate.Horizontal(_cl["txt"], "Return to Main Menu"))
        
        cmd = get_inpt("navi@nukebot:~#").strip().lower()
        
        if cmd == "1":
            try:
                if os.name == 'nt':
                    subprocess.Popen([sys.executable, "modules/nbot.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    subprocess.Popen([sys.executable, "modules/nbot.py"])
                print(Colorate.Horizontal(_cl["head"], "  [+] Bot started in a new terminal window!"))
            except Exception as e:
                print(Colorate.Horizontal(_cl["num"], f"  [!] Error starting bot: {e}"))
            time.sleep(2)
            
        elif cmd == "2":
            try:
                if os.path.exists(config_path):
                    os.startfile(os.path.abspath(config_path))
                    print(Colorate.Horizontal(_cl["head"], "  [+] botcfg.json opened!"))
                else:
                    print(Colorate.Horizontal(_cl["num"], "  [!] Configuration file does not exist!"))
            except Exception as e:
                print(Colorate.Horizontal(_cl["num"], f"  [!] Error opening file: {e}"))
            time.sleep(1.5)
            
        elif cmd == "3":
            print_banner()
            print(Colorate.Horizontal(_cl["head"], "  [ NUKE BOT HELP ]\n"))
            print(Colorate.Horizontal(_cl["txt"], "  The Nuke Bot runs in a separate console window and responds to Discord commands:"))
            print(Colorate.Horizontal(_cl["num"], "  • .kill   ") + Colorate.Horizontal(_cl["txt"], "- Deletes guild channels and spams/bans (Configurable)."))
            print(Colorate.Horizontal(_cl["num"], "  • .massban") + Colorate.Horizontal(_cl["txt"], "- Bans all non-admin members in the server."))
            print(Colorate.Horizontal(_cl["num"], "  • .erase  ") + Colorate.Horizontal(_cl["txt"], "- Deletes all channels in the guild."))
            print(Colorate.Horizontal(_cl["txt"], "\n  Configurable values are stored in core/botcfg.json."))
            input("\n  Press Enter to continue...")
            
        elif cmd == "99":
            break

def run_app():
    while 1:
        _cl = Theme.get_colors()
        print_banner()
        _cfg = get_config()
        if _cfg.get("theme", "blue").lower().startswith("modern"):
            from core.modern_ui import ModernUI as _mui
            _d_i = ["[1] Webhook Tools", "[2] Token Tools", "[3] Nitro Generator", "[4] Server Info", "[5] Bot Invite Gen", "[6] Selfbot", "[7] Server Cloner", "[8] Nuke Bot"]
            _o_i = ["[10] Port Scanner", "[11] Whois Lookup", "[12] DNS Lookup", "[14] Dox Tracker", "[15] Dox Creator", "[16] Phone Lookup", "[17] Email Lookup"]
            _m_i = ["[20] Email Bomber", "[21] Crypto Clipper", "[22] Vuln Scanner", "[23] DDoS Attack", "[24] Stealer Builder", "[25] Keylogger Builder", "[26] IP Grabber", "[27] Rat Builder", "[28] Wallet Bruteforce"]
            _g_i = ["[30] Base64 Codec", "[31] System Info", "[32] IP Pinger", "[33] Obfuscator", "[13] Metadata Scan"]
            _r_i = ["[40] User Info", "[41] Cookie Info", "[42] Cookie Login", "[43] Group Info", "[44] Asset DL"]
            _f_i = ["[50] Faker Tools", "[34] Web Cloner", "[35] QR Code Gen"]
            _s_i = ["[60] Info", "[61] Config", "[99] Exit"]
            
            _mui.render_menu(Colorate, Theme, [("DISCORD", _d_i), ("OSINT", _o_i), ("MALICIOUS", _m_i)])
            print()
            _mui.render_menu(Colorate, Theme, [("GENERAL", _g_i), ("ROBLOX", _r_i), ("FAKER", _f_i), ("SYSTEM", _s_i)])
        else:
            print(Colorate.Horizontal(_cl["head"], "    [ DISCORD ]              [ OSINT ]                [ MALICIOUS ]"))
            _d = [("[1] Webhook Tools", "[10] Port Scanner", "[20] Email Bomber"),("[2] Token Tools", "[11] Whois Lookup", "[21] Crypto Clipper"),("[3] Nitro Generator", "[12] DNS Lookup", "[22] Vuln Scanner"),("[4] Server Info", "[14] Dox Tracker", "[23] DDoS Attack"),("[5] Bot Invite Gen", "[15] Dox Creator", "[24] Stealer Builder"), ("[6] Selfbot", "[16] Phone Lookup", "[25] Keylogger Builder"), ("[7] Server Cloner", "[17] Email Lookup", "[26] IP Grabber"), ("[8] Nuke Bot", "", "[27] Rat Builder"), ("", "", "[28] Wallet Bruteforce")]
            for _r1, _r2, _r3 in _d:
                def _f(s, w):
                    if not s: return " " * w
                    _p = s.find(']') + 2 if ']' in s else 0
                    return Colorate.Horizontal(_cl["num"], s[:_p]) + Colorate.Horizontal(_cl["txt"], f"{s[_p:]:<{w-_p}}")
                print(f"    {_f(_r1, 25)}{_f(_r2, 25)}{_f(_r3, 20)}")
            print("\n" + Colorate.Horizontal(_cl["head"], "    [ GENERAL ]              [ ROBLOX ]               [ FAKER ]               [ SYSTEM ]"))
            _g = [("[30] Base64 Codec", "[40] User Info", "[50] Faker Tools", "[60] Info"),("[31] System Info", "[41] Cookie Info", "[34] Web Cloner", "[61] Config"),("[32] IP Pinger", "[42] Cookie Login", "[35] QR Code Gen", "[99] Exit"),("[33] Obfuscator", "[43] Group Info", "", ""),("[13] Metadata Scan", "[44] Asset DL", "", "")]
            for _r1, _r2, _r3, _r4 in _g:
                print(f"    {_f(_r1, 25)}{_f(_r2, 25)}{_f(_r3, 24)}{_f(_r4, 20)}")
        _c = get_inpt()
        if _c == "1":
            while 1:
                print_banner()
                print(Colorate.Horizontal(_cl["head"], "  [ WEBHOOK OPERATIONS ]\n"))
                menu_opts({"1": "Spammer", "2": "Deleter", "99": "Return"})
                _cc = get_inpt("navi@discord/webhooks:~#")
                if _cc == "1": webhook_spam(get_inpt("url:"), get_inpt("msg:"), int(get_inpt("amt (10):") or 10))
                elif _cc == "2": webhook_delete(get_inpt("url:"))
                elif _cc == "99": break
        elif _c == "2":
            while 1:
                print_banner()
                print(Colorate.Horizontal(_cl["head"], "  [ TOKEN & ACCOUNT TOOLS ]\n"))
                menu_opts({"1": "Token Bruteforce", "2": "Token Info", "3": "Token Nuker", "4": "Token Login", "5": "Status Rotator", "6": "Token Onliner", "7": "Selfbot", "8": "Username Checker", "9": "Report Bot", "10": "Server Cloner", "99": "Return"})
                _cc = get_inpt("navi@discord/tokens:~#")
                if _cc == "1":
                    id_to_token()

                elif _cc == "2":
                    from modules.discord_tools import token_info
                    token_info(get_inpt("Token:"))
                elif _cc == "3":
                    from modules.discord_tools import token_nuker
                    token_nuker(get_inpt("Token:"))
                elif _cc == "4":
                    from modules.discord_tools import token_login
                    token_login(get_inpt("Token:"))
                elif _cc == "5":
                    from modules.discord_tools import token_rotator
                    token_rotator(get_inpt("Token:"))
                elif _cc == "6":
                    from modules.discord_tools import token_onliner
                    token_onliner()
                elif _cc == "7":
                    from modules.discord_tools import selfbot_menu
                    selfbot_menu()
                elif _cc == "8":
                    from modules.discord_tools import discord_username_checker
                    discord_username_checker(int(get_inpt("Threads (1):") or 1))
                elif _cc == "9":
                    from modules.discord_tools import discord_report_bot
                    discord_report_bot()
                elif _cc == "10":
                    from modules.discord_tools import discord_server_cloner
                    discord_server_cloner(get_inpt("Token:"))
                elif _cc == "99": break
        elif _c == "6":
            from modules.discord_tools import selfbot_menu
            selfbot_menu()
        elif _c == "7":
            from modules.discord_tools import discord_server_cloner
            discord_server_cloner(get_inpt("Token:"))
        elif _c == "8":
            _nbot_ui()
        elif _c == "3": nitro_generator(int(get_inpt("Threads (1):") or 1))
        elif _c == "4":
            from modules.discord_tools import server_info_lookup
            server_info_lookup(get_inpt("Invite Link:"))
        elif _c == "5":
            from modules.discord_tools import bot_invite_gen
            bot_invite_gen(get_inpt("Bot ID:"))
        elif _c == "10":
            _res = do_port_check(get_inpt("host:"))
            if not _res: print(Colorate.Horizontal(_cl["num"], "  [!] None found."))
            else: [print(Colorate.Horizontal(_cl["head"], f"  [+] Port {p} OPEN")) for p in _res]
            input("\n  Enter...")
        elif _c == "11":
            _inf = whois_lookup(get_inpt("ip/domain:"))
            if not _inf or "ERR" in _inf: print(Colorate.Horizontal(_cl["num"], f"  [!] Error: {_inf.get('ERR', '??')}"))
            else: [print(Colorate.Horizontal(_cl["num"], f"  {k:<15}: ") + Colorate.Horizontal(_cl["txt"], str(v))) for k, v in _inf.items()]
            input("\n  Enter...")
        elif _c == "12":
            _r = dns_lookup(get_inpt("host:"))
            for _k, _v in _r.items(): print(Colorate.Horizontal(_cl["num"], f"  {_k}: ") + Colorate.Horizontal(_cl["txt"], str(_v)))
            input("\n  Enter...")
        elif _c == "13":
            metadata_init()
        elif _c == "14":
            from modules.dox import dox_tracker
            dox_tracker()
        elif _c == "15":
            from modules.dox import dox_creator
            dox_creator()
        elif _c == "16":
            from modules.lookup import phone_track
            phone_track()
        elif _c == "17":
            from modules.osint import email_lookup_init
            email_lookup_init()


        elif _c == '20': mail_bomb(get_inpt("email:"), int(get_inpt("amt:") or 10)); input("\n  Enter...")
        elif _c == '21':
            from modules.malicious import build_clipper
            build_clipper(); input("\n  Enter...")
        elif _c == '22':
            from modules.malicious import sql_scanner
            sql_scanner()
        elif _c == '23':
            from modules.malicious import start_brute
            start_brute()
        elif _c == '24':
            subprocess.run([sys.executable, "modules/builder/builder_gui.py"])
        elif _c == '25':
            from modules.keylogger import build_keylogger
            build_keylogger()
        elif _c == '26':
            from modules.malicious import ip_grabber
            ip_grabber()
        elif _c == '27':
            from modules.builder.rat_builder import rat_builder_init
            rat_builder_init()
        elif _c == '28':
            from modules.wallet_scanner import wallet_scanner_init
            wallet_scanner_init()
        elif _c == '30':
            _m, _t = get_inpt("(E/D):").upper(), get_inpt("Text:")
            try: print(Colorate.Horizontal(_cl["head"], f"  Res: {CryptXer.b64_e(_t) if _m == 'E' else CryptXer.b64_d(_t)}"))
            except: pass
            input("\n  Enter...")
        elif _c == '31':
            _inf = get_sys_data()
            for _k, _v in _inf.items(): print(Colorate.Horizontal(_cl["num"], f"  {_k}: ") + Colorate.Horizontal(_cl["txt"], str(_v)))
            input("\n  Enter...")
        elif _c == '32':
            from modules.osint import ip_pinger
            ip_pinger()
        elif _c == '33':
            obfuscator_init()
        elif _c == '34':
            from modules.network import clone_website
            clone_website(get_inpt("URL to clone:"))
        elif _c == '40':
            from modules.roblox import roblox_user_info
            roblox_user_info()
        elif _c == '41':
            from modules.roblox import roblox_cookie_info
            roblox_cookie_info()
        elif _c == '42':
            from modules.roblox import roblox_cookie_login
            roblox_cookie_login()
        elif _c == '43':
            from modules.roblox import roblox_group_info
            roblox_group_info()
        elif _c == '44':
            from modules.roblox import roblox_asset_dl
            roblox_asset_dl()
        elif _c == '35':
            from modules.faker import fake_qr_gen
            fake_qr_gen()
        elif _c == "50":
            while 1:
                print_banner()
                print(Colorate.Horizontal(_cl["head"], "  [ FAKER & SIMULATIONS ]\n"))
                menu_opts({
                    "1": "Fake Token Gen", "2": "Fake Mail Gen", "3": "Fake Identity", 
                    "4": "Fake Nitro", "5": "Fake DDoS", "6": "Fake Credit Cards", 
                    "7": "Fake Wallet Miner", "8": "Social Botter", "9": "Fake PayPal OTP",
                    "10": "Fake Account Gen", "11": "Fake Fortnite Check", "12": "Fake Exodus",
                    "13": "Hacker Terminal", "14": "Ransomware Sim", "15": "Fake Bruteforcer",
                    "16": "QR Code Gen", "17": "Explanation", "99": "Return"
                })
                _cc = get_inpt("navi@faker:~#")
                if _cc == "1": from modules.faker import fake_token_gen; fake_token_gen()
                elif _cc == "2": from modules.faker import fake_mail_gen; fake_mail_gen()
                elif _cc == "3": from modules.faker import fake_identity_gen; fake_identity_gen()
                elif _cc == "4": from modules.faker import fake_nitro_gen; fake_nitro_gen()
                elif _cc == "5": from modules.faker import fake_ddos; fake_ddos()
                elif _cc == "6": from modules.faker import fake_cc_gen; fake_cc_gen()
                elif _cc == "7": from modules.faker import fake_wallet_miner; fake_wallet_miner()
                elif _cc == "8": from modules.faker import social_botter; social_botter()
                elif _cc == "9": from modules.faker import fake_paypal_otp; fake_paypal_otp()
                elif _cc == "10": from modules.faker import fake_account_gen; fake_account_gen()
                elif _cc == "11": from modules.faker import fake_fortnite_checker; fake_fortnite_checker()
                elif _cc == "12": from modules.faker import fake_exodus; fake_exodus()
                elif _cc == "13": from modules.faker import fake_hacker_typer; fake_hacker_typer()
                elif _cc == "14": from modules.faker import fake_ransomware; fake_ransomware()
                elif _cc == "15": from modules.faker import fake_bruteforcer; fake_bruteforcer()
                elif _cc == "16": from modules.faker import fake_qr_gen; fake_qr_gen()
                elif _cc == "17": from modules.faker import faker_explanation; faker_explanation()
                elif _cc == "99": break
        elif _c == "60": inf_view()
        elif _c == "61": cfg_mgr()
        elif _c == "99": sys.exit(0)

if __name__ == '__main__':
    init_os()
    boot_anim()
    _pre()
    threading.Thread(target=_pop, daemon=True).start()
    run_app()
