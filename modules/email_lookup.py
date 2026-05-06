#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import dns.resolver, re, time, requests, threading
from core.display import get_inpt, Colorate, Theme

_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

class Scanner:
    def __init__(self, email):
        self.e = email
        self.h = {"User-Agent": _UA}
        self.f = []
        self.l = threading.Lock()

    def _req(self, u, m="GET", d=None, h=None, p=None):
        try:
            _h = self.h.copy()
            if h: _h.update(h)
            r = requests.request(m, u, headers=_h, data=d, params=p, timeout=8)
            return r
        except: return None

    def ig(self):
        r = self._req("https://www.instagram.com/accounts/emailsignup/")
        if not r: return
        t = r.cookies.get('csrftoken')
        if not t: return
        _h = {"x-csrftoken": t, "Referer": "https://www.instagram.com/accounts/emailsignup/"}
        r = self._req("https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/", "POST", {"email": self.e}, _h)
        if r and ("email_is_taken" in r.text or "Another account" in r.text):
            with self.l: self.f.append("Instagram")

    def tw(self):
        r = self._req(f"https://api.twitter.com/i/users/email_available.json?email={self.e}")
        if r and r.json().get("taken"):
            with self.l: self.f.append("Twitter")

    def sp(self):
        r = self._req(f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={self.e}")
        if r and r.json().get("status") == 20:
            with self.l: self.f.append("Spotify")

    def ph(self):
        r = self._req("https://www.pornhub.com/signup")
        if not r: return
        try:
            import bs4
            t = bs4.BeautifulSoup(r.text, "html.parser").find("input", {"name": "token"})["value"]
            r = self._req(f"https://www.pornhub.com/user/create_account_check?token={t}", "POST", {"check_what": "email", "email": self.e})
            if r and "Email has been taken" in r.text:
                with self.l: self.f.append("PornHub")
        except: pass

    def pin(self):
        r = self._req("https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/", p={"source_url": "/", "data": '{"options": {"email": "' + self.e + '"}, "context": {}}'})
        if r and r.json().get("resource_response", {}).get("data"):
            with self.l: self.f.append("Pinterest")

    def img(self):
        r = self._req("https://imgur.com/signin/ajax_email_available", "POST", {"email": self.e}, {"X-Requested-With": "XMLHttpRequest"})
        if r and not r.json().get("data", {}).get("available"):
            with self.l: self.f.append("Imgur")

def email_lookup_init():
    cl = Theme.get_colors()
    t = get_inpt("target@email:~#")
    if not t or '@' not in t: return
    
    d = t.split('@')[-1]
    print(Colorate.Horizontal(cl["head"], f"  [*] Fetching DNS records for {d}..."))
    
    def _q(domain, type):
        try:
            r = dns.resolver.resolve(domain, type)
            return [str(i).strip('"') for i in r]
        except: return []

    mx = _q(d, 'MX')
    spf_recs = _q(d, 'TXT')
    
    print(f"\n{Colorate.Horizontal(cl['head'], '  [ DOMAIN INTEL ]')}")
    _l = lambda k, v: print(Colorate.Horizontal(cl["num"], f"  {k:<12} -> ") + Colorate.Horizontal(cl["txt"], str(v)))
    
    _l("TARGET", t)
    if mx:
        for m in mx: _l("MX_SRV", m)
    
    spf = "N/A"
    for s in spf_recs:
        if "v=spf1" in s: spf = s; break
    _l("SPF_REC", spf)
    
    s = Scanner(t)
    print(f"\n{Colorate.Horizontal(cl['head'], '  [*] Scanning social footprints...')}")
    
    tasks = [s.ig, s.tw, s.sp, s.ph, s.pin, s.img]
    threads = [threading.Thread(target=x) for x in tasks]
    for _t in threads: _t.start()
    for _t in threads: _t.join()
    
    if s.f:
        print(Colorate.Horizontal(cl["head"], f"  [+] Found on {len(s.f)} platforms:"))
        for plat in s.f:
            print(Colorate.Horizontal(cl["num"], "  [>] ") + Colorate.Horizontal(cl["txt"], plat))
    else:
        print(Colorate.Horizontal(cl["num"], "  [!] No social footprints found."))
    
    input(Colorate.Horizontal(cl["head"], "\n  [ BACK ]"))
