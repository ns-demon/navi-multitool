#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import os, sys
from core.display import Theme, Colorate, get_inpt

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except:
    os.system("pip install phonenumbers -q")
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone

def _w_log(m, s='+'):
    c = Theme.get_colors()
    return f" {Colorate.Horizontal(c['num'], f'[{s}]')} {Colorate.Horizontal(c['txt'], m)}"

def NumberInfo(p_num):
    try:
        p = phonenumbers.parse(p_num, None)
        return {
            "Carrier": carrier.name_for_number(p, "en"),
            "Type": "Mobile" if phonenumbers.number_type(p) == phonenumbers.PhoneNumberType.MOBILE else "Fixed",
            "Region": phonenumbers.region_code_for_number(p),
            "Location": geocoder.description_for_number(p, "en"),
            "Timezone": timezone.time_zones_for_number(p)[0] if timezone.time_zones_for_number(p) else "N/A"
        }
    except: return None

def phone_track():
    cl = Theme.get_colors()
    from core.display import print_banner
    print_banner()
    print(Colorate.Horizontal(cl["head"], "  [ PHONE TRACKER ]\n"))
    
    n = get_inpt("number (ex: +1234567890):")
    print(Colorate.Horizontal(cl["head"], f"\n  [+] Analyzing {n}...\n"))
    
    res = NumberInfo(n)
    if res:
        for k, v in res.items():
            print(f"  {Colorate.Horizontal(cl['num'], f'{k:<12}')} : {Colorate.Horizontal(cl['txt'], v)}")
    else:
        print(Colorate.Horizontal(cl["num"], "  [!] Invalid number format."))
        
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
