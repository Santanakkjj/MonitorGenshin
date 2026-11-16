import os
import sys

import win32com.client


def get_startup_folder():
    return os.path.join(
        os.environ["APPDATA"],
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )

def enable_startup():
    startup_folder = get_startup_folder()

    exe_path = sys.executable

    shortcut_path = os.path.join(
        startup_folder,
        "Monitor Genshin.lnk"
    )

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)

    shortcut.TargetPath = exe_path
    shortcut.WorkingDirectory = os.path.dirname(exe_path)
    shortcut.Description = "Monitor do Genshin"

    shortcut.save()

def disable_startup():
    shortcut_path = os.path.join(
        get_startup_folder(),
        "Monitor Genshin.lnk"
    )

    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)