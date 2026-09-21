import ollama
import json
from config import SYSTEM_PROMPT
from tools import execute


def ask(command):
    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": command}
        ]
    )
    return response["message"]["content"]


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