import subprocess
import os
import time
import pyautogui
import pygetwindow as gw
from config import ALLOWED_APPS


def execute(parsed):
    tool = parsed.get("tool")
    arg = parsed.get("arg", "")

    if tool == "open_app":
        _open_app(arg)
    elif tool == "close_app":
        _close_app(arg)
    elif tool == "list_files":
        _list_files(arg)
    elif tool == "type_text":
        _type_text(arg)
    else:
        print("   UNKNOWN command, kuch nahi kiya.")


def _open_app(arg):
    if arg not in ALLOWED_APPS:
        print(f"   BLOCKED: '{arg}' whitelist mein nahi hai.")
        return
    confirm = input(f"   '{arg}' kholun? (Y/N): ")
    if confirm.strip().lower() == "y":
        subprocess.Popen(f'start "" "{ALLOWED_APPS[arg]}"', shell=True)
        print(f"   DONE: {arg} khul gaya.")
    else:
        print("   CANCELLED by user.")


def _close_app(arg):
    if arg not in ALLOWED_APPS:
        print(f"   BLOCKED: '{arg}' whitelist mein nahi hai.")
        return
    confirm = input(f"   '{arg}' band karun? (Y/N): ")
    if confirm.strip().lower() == "y":
        exe_name = ALLOWED_APPS[arg]
        subprocess.run(f'taskkill /IM "{exe_name}" /F', shell=True)
        print(f"   DONE: {arg} band ho gaya.")
    else:
        print("   CANCELLED by user.")


def _list_files(arg):
    path = os.path.expanduser(f"~/{arg}")
    confirm = input(f"   '{path}' ki files dikhaun? (Y/N): ")
    if confirm.strip().lower() == "y":
        try:
            for f in os.listdir(path):
                print("     -", f)
        except FileNotFoundError:
            print(f"   ERROR: '{path}' nahi mila.")
    else:
        print("   CANCELLED by user.")


def _type_text(arg):
    windows = gw.getWindowsWithTitle("Notepad")
    if not windows:
        print("   ERROR: Notepad khula hua nahi mila. Pehle 'open notepad' chalao.")
        return
    confirm = input(f"   Ye type karun: '{arg}'? (Y/N): ")
    if confirm.strip().lower() == "y":
        notepad_window = windows[0]
        notepad_window.activate()
        time.sleep(0.5)
        pyautogui.write(arg, interval=0.03)
        print("   DONE: text Notepad mein type ho gaya.")
    else:
        print("   CANCELLED by user.")