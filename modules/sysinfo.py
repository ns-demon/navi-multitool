#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import platform, os, ctypes

def get_sys_data():
    d = {"System": platform.system(), "Release": platform.release(), "Machine": platform.machine()}
    try: a = os.getuid() == 0
    except:
        try: a = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except: a = False
    d["Privileged"] = str(a)
    return d
