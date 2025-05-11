
import socket
import json
from pathlib import Path

class PhoenixBotClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.create_connection((self.host, self.port))

    def send_message(self, message):
        if self.socket:
            msg = json.dumps(message) + '\x01'
            self.socket.sendall(msg.encode('utf-8'))

    def close(self):
        if self.socket:
            self.socket.close()

def find_phoenix_clients():
    print("[DEBUG] Szukam pliku PhoenixIPC.json...")
    possible_paths = [
        Path.home() / "AppData" / "Roaming" / "PhoenixBot" / "PhoenixIPC.json",
        Path("C:/ProgramData/PhoenixBot/PhoenixIPC.json"),
        Path.cwd() / "PhoenixIPC.json"
    ]
    for path in possible_paths:
        print(f"[DEBUG] Sprawdzam: {path}")
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(f"[DEBUG] Zawartość JSON: {data}")
                    return data
            except Exception as e:
                print(f"[ERROR] Błąd przy czytaniu {path}: {e}")
    print("[WARNING] Nie znaleziono aktywnego klienta PhoenixBot.")
    return []
