#  _   _                 _
# | \ | |               (_)
# |  \| | __ ___   __ _  _
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
#
# Navi Multitool - System Information Module

import os
import ctypes
import platform
import subprocess
import time
import socket

import psutil


def safe_run(cmd):
    try:
        return subprocess.check_output(
            cmd,
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "Unknown"


def get_gpu():
    if platform.system() == "Windows":
        return safe_run(
            'powershell -Command "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"'
        )

    return "Unsupported"


def get_cpu():
    try:
        import cpuinfo
        return cpuinfo.get_cpu_info().get(
            "brand_raw",
            platform.processor()
        )
    except Exception:
        return platform.processor() or "Unknown"


def get_bios():
    if platform.system() == "Windows":
        return safe_run(
            'powershell -Command "Get-CimInstance Win32_BIOS | Select-Object -ExpandProperty SMBIOSBIOSVersion"'
        )

    return "Unknown"


def is_admin():
    try:
        if platform.system() == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except Exception:
        return False


def get_battery():
    try:
        battery = psutil.sensors_battery()

        if battery:
            status = "Charging" if battery.power_plugged else "Discharging"
            return f"{battery.percent}% ({status})"

    except Exception:
        pass

    return "No battery detected"


def get_sys_data():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    boot_time = time.time() - psutil.boot_time()

    hours, rem = divmod(boot_time, 3600)
    minutes, seconds = divmod(rem, 60)

    data = {
        "OS": f"{platform.system()} {platform.release()}",
        "Version": platform.version(),
        "Architecture": platform.architecture()[0],
        "Machine": platform.machine(),

        "CPU": get_cpu(),
        "CPU Usage": f"{psutil.cpu_percent(interval=1)}%",
        "CPU Cores": (
            f"{psutil.cpu_count(logical=False)} physical / "
            f"{psutil.cpu_count()} logical"
        ),

        "RAM Total": f"{memory.total / (1024**3):.2f} GB",
        "RAM Used": f"{memory.used / (1024**3):.2f} GB",
        "RAM Usage": f"{memory.percent}%",

        "Disk": (
            f"{disk.used / (1024**3):.2f}GB / "
            f"{disk.total / (1024**3):.2f}GB "
            f"({disk.percent}%)"
        ),

        "GPU": get_gpu(),
        "BIOS": get_bios(),

        "Hostname": socket.gethostname(),
        "Local IP": socket.gethostbyname(socket.gethostname()),

        "Battery": get_battery(),

        "Uptime": (
            f"{int(hours)}h "
            f"{int(minutes)}m "
            f"{int(seconds)}s"
        ),

        "Administrator": str(is_admin())
    }

    return data


def print_sys_data():
    data = get_sys_data()

    print("\n========== SYSTEM INFO ==========\n")

    for key, value in data.items():
        print(f"{key:<18}: {value}")

    print("\n=================================\n")


if __name__ == "__main__":
    print_sys_data()