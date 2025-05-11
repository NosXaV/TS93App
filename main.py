
import tkinter as tk
from tkinter import ttk, messagebox
from phoenix_api import PhoenixBotClient, find_phoenix_clients
import json

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TS93 Automator - stworzony przez ChatGPT i XaV")
        self.geometry("500x350")
        self.client = None

        ttk.Label(self, text="Wybierz klienta Phoenix Bot:").pack(pady=5)
        self.clients = find_phoenix_clients()
        self.client_var = tk.StringVar()
        self.client_box = ttk.Combobox(self, textvariable=self.client_var, state="readonly")
        self.client_box['values'] = [f"{c['name']} (port {c['port']})" for c in self.clients]
        self.client_box.pack(pady=5)

        self.auto_repeat = tk.BooleanVar()
        ttk.Checkbutton(self, text="Powtarzaj TS automatycznie", variable=self.auto_repeat).pack(pady=5)
        ttk.Button(self, text="Połącz i rozpocznij", command=self.start).pack(pady=10)

    def start(self):
        if not self.clients or not self.client_box.get():
            messagebox.showerror("Błąd", "Nie wybrano klienta Phoenix Bot.")
            return

        selected_index = self.client_box.current()
        client_info = self.clients[selected_index]

        try:
            self.client = PhoenixBotClient("127.0.0.1", client_info["port"])
            self.client.connect()

            with open("ts93_script.json", "r", encoding="utf-8") as f:
                steps = json.load(f)["steps"]

            self.run_steps(steps)
            if self.auto_repeat.get():
                self.after(1000, self.start)  # Restartuj po 1s

        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def run_steps(self, steps):
        for step in steps:
            self.client.send_message(step)

if __name__ == "__main__":
    app = App()
    app.mainloop()
