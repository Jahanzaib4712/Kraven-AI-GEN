import ollama
import json
import subprocess
import pyautogui
import time
import pygetwindow as gw

SYSTEM_PROMPT = """You are a command interpreter. You ONLY respond with valid JSON, nothing else.
Available tools:
- open_app(name): opens an application
- close_app(name): closes an application
- list_files(path): lists files in a folder
- type_text(content): types text into the currently open app

Respond ONLY in this exact format:
{"tool": "tool_name", "arg": "value"}

If the command doesn't match any tool, respond:
{"tool": "unknown", "arg": ""}
"""

# Whitelist — sirf ye apps khulne ki ijazat hai
ALLOWED_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "vscode": "code",
    "code": "code",
}

def ask(command):
    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": command}
        ]
    )
    return response["message"]["content"]

def execute(parsed):
    tool = parsed.get("tool")
    arg = parsed.get("arg", "")

    if tool == "open_app":
        if arg not in ALLOWED_APPS:
            print(f"   BLOCKED: '{arg}' whitelist mein nahi hai.")
            return
        confirm = input(f"   '{arg}' kholun? (Y/N): ")
        if confirm.strip().lower() == "y":
            subprocess.Popen(f'start "" "{ALLOWED_APPS[arg]}"', shell=True)
            print(f"   DONE: {arg} khul gaya.")
        else:
            print("   CANCELLED by user.")

    elif tool == "close_app":
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

    elif tool == "list_files":
        import os
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

    elif tool == "type_text":
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

    else:
        print("   UNKNOWN command, kuch nahi kiya.")

# ---- Live loop ----
print("Command do (exit likh ke rukna):")
while True:
    cmd = input("\n> ")
    if cmd.strip().lower() == "exit":
        break
    raw = ask(cmd)
    try:
        parsed = json.loads(raw)
        print(f"   Model ne samjha: {parsed}")
        execute(parsed)
    except json.JSONDecodeError:
        print("   ERROR: model ka jawab JSON nahi tha:", raw)