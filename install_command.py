import os
import sys
import shutil
import stat
from pathlib import Path

def get_platform():
    if sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform.startswith('darwin'):
        return 'macos'
    elif sys.platform.startswith('linux'):
        return 'linux'
    else:
        raise OSError(f"Unsupported platform: {sys.platform}")

def is_admin_windows():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin_windows():
    import ctypes
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:])
    
    ctypes.windll.shell32.ShellExecuteW(
        None, 
        "runas", 
        sys.executable, 
        params,
        None, 
        1
    )

def create_windows_batch_files(ytgrabber_dir, batch_dir):
    commands = ["ytgrabber", "ytgrab"]
    for cmd in commands:
        batch_content = f"""@echo off
cd /d "{ytgrabber_dir}"
powershell -ExecutionPolicy Bypass -File "quickstart.ps1" %*"""
        
        with open(os.path.join(batch_dir, f"{cmd}.bat"), "w") as f:
            f.write(batch_content)

def create_unix_shell_scripts(ytgrabber_dir, scripts_dir):
    commands = ["ytgrabber", "ytgrab"]
    for cmd in commands:
        script_content = f"""#!/bin/bash
cd "{ytgrabber_dir}"
./quickstart.sh "$@"
"""
        script_path = os.path.join(scripts_dir, cmd)
        with open(script_path, "w") as f:
            f.write(script_content)
        # Make the script executable
        st = os.stat(script_path)
        os.chmod(script_path, st.st_mode | stat.S_IEXEC)

def add_to_windows_path(directory):
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
        try:
            path, _ = winreg.QueryValueEx(key, "Path")
        except WindowsError:
            path = ""
        
        paths = path.split(";") if path else []
        if directory not in paths:
            paths.append(directory)
            new_path = ";".join(p for p in paths if p)
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)

def modify_unix_path(add=True):
    home = str(Path.home())
    shell_rc_files = []
    
    if os.path.exists(os.path.join(home, '.zshrc')):
        shell_rc_files.append('.zshrc')
    if os.path.exists(os.path.join(home, '.bashrc')):
        shell_rc_files.append('.bashrc')
    
    if not shell_rc_files:
        shell_rc_files.append('.bashrc')
    
    scripts_dir = os.path.join(home, '.local', 'bin')
    path_line = f'\nexport PATH="$PATH:{scripts_dir}"\n'
    
    for rc_file in shell_rc_files:
        rc_path = os.path.join(home, rc_file)
        if add:
            # Add to PATH if not already present
            if os.path.exists(rc_path):
                with open(rc_path, 'r') as f:
                    content = f.read()
                if scripts_dir not in content:
                    with open(rc_path, 'a') as f:
                        f.write(path_line)
            else:
                with open(rc_path, 'w') as f:
                    f.write(path_line)

def setup():
    platform = get_platform()
    ytgrabber_dir = os.path.dirname(os.path.abspath(__file__))
    
    if platform == 'windows':
        if not is_admin_windows():
            run_as_admin_windows()
            return
        
        batch_dir = os.path.join(os.path.expanduser("~"), ".ytgrabber")
        os.makedirs(batch_dir, exist_ok=True)
        create_windows_batch_files(ytgrabber_dir, batch_dir)
        add_to_windows_path(batch_dir)
        print(f"Successfully installed ytgrabber commands to {batch_dir}")
        
    else:
        scripts_dir = os.path.join(str(Path.home()), '.local', 'bin')
        os.makedirs(scripts_dir, exist_ok=True)
        create_unix_shell_scripts(ytgrabber_dir, scripts_dir)
        modify_unix_path(add=True)
        print(f"Successfully installed ytgrabber commands to {scripts_dir}")
        print("Please restart your terminal or run 'source ~/.bashrc' (or ~/.zshrc) to use the commands")

if __name__ == "__main__":
    setup()
