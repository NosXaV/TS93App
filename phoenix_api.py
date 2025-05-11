import json

class PhoenixBotAPI:
    def __init__(self, client_name):
        self.client_name = client_name

    def run_ts93(self):
        print(f"[PhoenixBotAPI] Uruchamianie TS 93 dla klienta {self.client_name}...")
        
        try:
            with open("ts93_script.json", "r", encoding="utf-8") as f:
                script = json.load(f)

            for step in script.get("steps", []):
                print(f" -> Wykonuję: {step['action']} | Parametry: {step.get('params', {})}")

        except FileNotFoundError:
            print("Nie znaleziono pliku ts93_script.json")
        except Exception as e:
            print(f"Błąd podczas wykonywania TS93: {e}")
