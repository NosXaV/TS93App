import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from phoenix_api import PhoenixBotAPI

class TS93BotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TS93 Bot - ChatGPT & XaV")
        self.bot_api = None
        self.auto_repeat = tk.BooleanVar()
        self.is_running = False

        self.build_gui()

    def build_gui(self):
        self.client_label = ttk.Label(self.root, text="Wybierz klienta Phoenix Bota:")
        self.client_label.pack(pady=5)

        self.client_combo = ttk.Combobox(self.root, values=["Client1", "Client2"], state="readonly")
        self.client_combo.pack(pady=5)

        self.connect_button = ttk.Button(self.root, text="Połącz", command=self.connect_to_client)
        self.connect_button.pack(pady=5)

        self.start_button = ttk.Button(self.root, text="Uruchom TS 93", command=self.start_ts, state="disabled")
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(self.root, text="Zatrzymaj", command=self.stop_ts, state="disabled")
        self.stop_button.pack(pady=5)

        self.repeat_check = ttk.Checkbutton(self.root, text="Powtarzaj automatycznie", variable=self.auto_repeat)
        self.repeat_check.pack(pady=5)

        self.signature = ttk.Label(self.root, text="Skrypt przygotowany przez ChatGPT oraz XaV", font=("Arial", 8))
        self.signature.pack(side="bottom", pady=5)

    def connect_to_client(self):
        client = self.client_combo.get()
        if not client:
            messagebox.showerror("Błąd", "Wybierz klienta Phoenix Bota.")
            return
        self.bot_api = PhoenixBotAPI(client)
        messagebox.showinfo("Sukces", f"Połączono z {client}")
        self.start_button.config(state="normal")

    def start_ts(self):
        if not self.bot_api:
            messagebox.showerror("Błąd", "Nie połączono z klientem.")
            return

        self.is_running = True
        self.stop_button.config(state="normal")
        threading.Thread(target=self.ts_loop, daemon=True).start()

    def stop_ts(self):
        self.is_running = False
        self.stop_button.config(state="disabled")

    def ts_loop(self):
        while self.is_running:
            self.bot_api.run_ts93()
            if not self.auto_repeat.get():
                break
            time.sleep(5)
        self.stop_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = TS93BotApp(root)
    root.mainloop()
