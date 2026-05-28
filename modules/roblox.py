#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import requests, json, time, os
from core.display import Colors, Colorate, get_inpt, Theme

def _hdr(): return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def roblox_user_info():
    cl = Theme.get_colors()
    un = get_inpt("roblox_username:")
    print(Colorate.Horizontal(cl["head"], "  [+] Fetching data..."))
    try:
        r = requests.post("https://users.roblox.com/v1/usernames/users", headers=_hdr(), json={"usernames": [un], "excludeBannedUsers": False})
        d = r.json()
        if not d['data']:
            print(Colorate.Horizontal(cl["num"], "  [!] User not found."))
            return
        res = requests.get(f"https://users.roblox.com/v1/users/{d['data'][0]['id']}", headers=_hdr()).json()
        ln = "  " + "─" * 50
        print(Colorate.Horizontal(cl["head"], ln))
        inf = [("Username", res.get("name")), ("ID", res.get("id")), ("Display", res.get("displayName")), ("Banned", res.get("isBanned")), ("Created", res.get("created")), ("Verified", res.get("hasVerifiedBadge"))]
        for k, v in inf:
            print(Colorate.Horizontal(cl["num"], f"  [>] {k:<12}: ") + Colorate.Horizontal(cl["txt"], str(v)))
        print(Colorate.Horizontal(cl["head"], ln))
    except Exception as e:
        print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def roblox_cookie_info():
    cl = Theme.get_colors()
    ck = get_inpt("roblox_cookie:")
    print(Colorate.Horizontal(cl["head"], "  [+] Validating cookie..."))
    try:
        r = requests.get("https://www.roblox.com/mobileapi/userinfo", headers=_hdr(), cookies={".ROBLOSECURITY": ck})
        if r.status_code != 200:
            print(Colorate.Horizontal(cl["num"], "  [!] Invalid Cookie."))
            return
        j = r.json()
        ln = "  " + "─" * 50
        print(Colorate.Horizontal(cl["head"], ln))
        inf = [("Username", j.get("UserName")), ("ID", j.get("UserID")), ("Robux", j.get("RobuxBalance")), ("Premium", j.get("IsPremium")), ("BC", j.get("IsAnyBuildersClubMember"))]
        for k, v in inf:
            print(Colorate.Horizontal(cl["num"], f"  [>] {k:<12}: ") + Colorate.Horizontal(cl["txt"], str(v)))
        print(Colorate.Horizontal(cl["head"], ln))
    except Exception as e:
        print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def roblox_cookie_login():
    cl = Theme.get_colors()
    ck = get_inpt("roblox_cookie:")
    print(Colorate.Horizontal(cl["head"], "  [+] Select Browser (1: Chrome, 2: Edge, 3: Firefox)"))
    b = get_inpt("browser:")
    try:
        from selenium import webdriver
        dr = None
        if b == '1': dr = webdriver.Chrome()
        elif b == '2': dr = webdriver.Edge()
        elif b == '3': dr = webdriver.Firefox()
        else: return
        print(Colorate.Horizontal(cl["head"], "  [+] Browser started. Injecting cookie..."))
        dr.get("https://www.roblox.com/Login")
        dr.add_cookie({"name": ".ROBLOSECURITY", "value": ck})
        dr.refresh()
        print(Colorate.Horizontal(cl["head"], "  [+] Logged in! Keeping browser open..."))
        input(Colorate.Horizontal(cl["head"], "  Press Enter to close browser and return."))
        dr.quit()
    except Exception as e:
        print(Colorate.Horizontal(cl["num"], f"  [!] Selenium error: {e}"))
        input("\n  Press Enter...")

def roblox_group_info():
    cl = Theme.get_colors()
    _id = get_inpt("group_id:")
    print(Colorate.Horizontal(cl["head"], "  [+] Fetching group data..."))
    try:
        r = requests.get(f"https://groups.roblox.com/v1/groups/{_id}", headers=_hdr()).json()
        if "id" not in r:
            print(Colorate.Horizontal(cl["num"], "  [!] Group not found."))
            return
        ln = "  " + "─" * 50
        print(Colorate.Horizontal(cl["head"], ln))
        inf = [("Name", r.get("name")), ("Owner", r.get("owner", {}).get("username")), ("Members", r.get("memberCount")), ("Public", r.get("publicEntryAllowed")), ("Locked", r.get("isLocked"))]
        for k, v in inf:
            print(Colorate.Horizontal(cl["num"], f"  [>] {k:<12}: ") + Colorate.Horizontal(cl["txt"], str(v)))
        print(Colorate.Horizontal(cl["head"], ln))
    except Exception as e: print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def roblox_asset_dl():
    cl = Theme.get_colors()
    _id = get_inpt("asset_id:")
    print(Colorate.Horizontal(cl["head"], "  [+] Downloading asset..."))
    try:
        r = requests.get(f"https://assetdelivery.roblox.com/v1/asset/?id={_id}", headers=_hdr())
        if r.status_code != 200:
            print(Colorate.Horizontal(cl["num"], "  [!] Asset not found."))
            return
        if not os.path.exists("output"): os.makedirs("output")
        with open(f"output/asset_{_id}.rbxm", "wb") as f: f.write(r.content)
        print(Colorate.Horizontal(cl["head"], f"  [+] Saved to: output/asset_{_id}.rbxm"))
    except Exception as e: print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def roblox_name_history():
    cl = Theme.get_colors()
    un = get_inpt("roblox_username:")
    print(Colorate.Horizontal(cl["head"], "  [+] Fetching name history..."))
    try:
        r = requests.post("https://users.roblox.com/v1/usernames/users", headers=_hdr(), json={"usernames": [un], "excludeBannedUsers": False})
        d = r.json()
        if not d.get('data'):
            print(Colorate.Horizontal(cl["num"], "  [!] User not found."))
            return
        uid = d['data'][0]['id']
        res = requests.get(f"https://users.roblox.com/v1/users/{uid}/username-history?limit=50&sortOrder=Desc", headers=_hdr())
        
        ln = "  " + "─" * 50
        print(Colorate.Horizontal(cl["head"], ln))
        
        if res.status_code == 200:
            hist = res.json().get("data", [])
            if not hist:
                print(Colorate.Horizontal(cl["num"], "  [>] No past usernames found."))
            else:
                for idx, entry in enumerate(hist):
                    print(Colorate.Horizontal(cl["num"], f"  [{idx+1}] ") + Colorate.Horizontal(cl["txt"], entry.get("name")))
        else:
            print(Colorate.Horizontal(cl["num"], "  [!] API Error or Private History."))
            
        print(Colorate.Horizontal(cl["head"], ln))
    except Exception as e:
        print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
