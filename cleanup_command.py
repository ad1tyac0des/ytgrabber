import os
import sys
import shutil
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

def remove_windows_batch_files():
    batch_dir = os.path.join(os.path.expanduser("~"), ".ytgrabber")
    if os.path.exists(batch_dir):
        shutil.rmtree(batch_dir)
    return batch_dir

def remove_from_windows_path(directory):
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
        try:
            path, _ = winreg.QueryValueEx(key, "Path")
        except WindowsError:
            return
        
        paths = path.split(";")
        paths = [p for p in paths if p and p != directory]
        new_path = ";".join(paths)
        
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)

def remove_unix_scripts():
    scripts_dir = os.path.join(str(Path.home()), '.local', 'bin')
    commands = ["ytgrabber", "ytgrab"]
    for cmd in commands:
        script_path = os.path.join(scripts_dir, cmd)
        if os.path.exists(script_path):
            os.remove(script_path)
    return scripts_dir

def modify_unix_path(add=False):
    home = str(Path.home())
    shell_rc_files = []
    
    # Get which shell config files to modify
    if os.path.exists(os.path.join(home, '.zshrc')):
        shell_rc_files.append('.zshrc')
    if os.path.exists(os.path.join(home, '.bashrc')):
        shell_rc_files.append('.bashrc')
    
    if not shell_rc_files:
        return
    
    scripts_dir = os.path.join(home, '.local', 'bin')
    path_line = f'export PATH="$PATH:{scripts_dir}"\n'
    
    for rc_file in shell_rc_files:
        rc_path = os.path.join(home, rc_file)
        if os.path.exists(rc_path):
            with open(rc_path, 'r') as f:
                lines = f.readlines()
            
            # Remove the PATH line if it exists
            lines = [line for line in lines if scripts_dir not in line]
            
            with open(rc_path, 'w') as f:
                f.writelines(lines)

def cleanup():
    platform = get_platform()
    
    if platform == 'windows':
        if not is_admin_windows():
            run_as_admin_windows()
            return
        
        batch_dir = remove_windows_batch_files()
        remove_from_windows_path(batch_dir)
        print(f"Successfully removed ytgrabber commands from {batch_dir}")
        
    else:  # macOS or Linux
        scripts_dir = remove_unix_scripts()
        modify_unix_path(add=False)
        print(f"Successfully removed ytgrabber commands from {scripts_dir}")
        print("Please restart your terminal or run 'source ~/.bashrc' (or ~/.zshrc) for the changes to take effect")

if __name__ == "__main__":
    cleanup()
