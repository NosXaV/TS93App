
import tkinter as tk
from tkinter import ttk, messagebox
from phoenix_api import PhoenixBotClient
import json

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TS93 Automator - stworzony przez ChatGPT i XaV")
        self.geometry("500x300")
        self.client = None

        ttk.Label(self, text="Adres IP klienta Phoenix Bot:").pack(pady=5)
        self.ip_entry = ttk.Entry(self)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.pack(pady=5)

        ttk.Label(self, text="Port klienta Phoenix Bot:").pack(pady=5)
        self.port_entry = ttk.Entry(self)
        self.port_entry.insert(0, "12345")
        self.port_entry.pack(pady=5)

        self.auto_repeat = tk.BooleanVar()
        ttk.Checkbutton(self, text="Powtarzaj TS automatycznie", variable=self.auto_repeat).pack(pady=5)

        ttk.Button(self, text="Połącz i rozpocznij", command=self.start).pack(pady=10)

    def start(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())

        try:
            self.client = PhoenixBotClient(ip, port)
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
