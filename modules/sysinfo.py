import platform, os, ctypes

def get_sys_data():
    d = {"System": platform.system(), "Release": platform.release(), "Machine": platform.machine()}
    try: a = os.getuid() == 0
    except:
        try: a = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except: a = False
    d["Privileged"] = str(a)
    return d
