
import tkinter as tk
from tkinter import messagebox, ttk

import config_manager
import startup


class Interface:
    def __init__(self, config):
        self.window = tk.Tk()

        # ==================================================
        # FONTES
        # ==================================================

        self.FONT_TITLE = ("Segoe UI", 20, "bold")
        self.FONT_SUBTITLE = ("Segoe UI", 15, "bold")
        self.FONT_NORMAL = ("Segoe UI", 11)
        self.FONT_SMALL = ("Segoe UI", 9)

        # ==================================================
        # CORES
        # ==================================================

        self.COLOR_BG = "#171D2B"
        self.COLOR_PANEL = "#222C3D"
        self.COLOR_INPUT = "#303D50"

        self.COLOR_GOLD = "#D8B46A"
        self.COLOR_BLUE = "#75B9D9"
        self.COLOR_PURPLE = "#9B83C9"
        self.COLOR_GREEN = "#70C99A"
        self.COLOR_RED = "#E47777"

        self.COLOR_TEXT = "#E8E1D5"
        self.COLOR_MUTED = "#A8B1C0"

        # ==================================================
        # CONFIGURAÇÃO DA JANELA
        # ==================================================

        self.window.title("Monitor Genshin")
        self.window.geometry("720x500")
        self.window.resizable(False, False)
        self.window.configure(bg=self.COLOR_BG)
        self.window.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.config = config

        # ==================================================
        # ESTILOS TTK
        # ==================================================

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Panel.TFrame",
            background=self.COLOR_PANEL
        )

        self.style.configure(
            "Vertical.TSeparator",
            background=self.COLOR_GOLD
        )

        # ==================================================

        self.create_frames()
        self.create_status()
        self.create_config()

    # ======================================================
    # FRAMES PRINCIPAIS
    # ======================================================

    def create_frames(self):
        self.frame_status = ttk.Frame(
            self.window,
            style="Panel.TFrame",
            padding=15
        )

        self.frame_config = ttk.Frame(
            self.window,
            style="Panel.TFrame",
            padding=15
        )

        self.separator = ttk.Separator(
            self.window,
            orient="vertical"
        )

        self.frame_status.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(20, 10),
            pady=20
        )

        self.frame_config.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(10, 20),
            pady=20
        )

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(2, weight=1)

        self.separator.grid(
            row=0,
            column=1,
            sticky="ns",
            pady=35
        )

    # ======================================================
    # STATUS
    # ======================================================

    def create_status(self):
        self.status_info = tk.StringVar(value="● Carregando...")
        self.runtime_info = tk.StringVar(value="--:--:--")

        self.last_open_info = tk.StringVar(
            value="Nenhuma abertura registrada."
        )

        # FRAMES
        self.frame_status_header = ttk.Frame(
            self.frame_status,
            style="Panel.TFrame"
        )

        self.frame_current_status = ttk.Frame(
            self.frame_status,
            style="Panel.TFrame"
        )

        self.frame_last_open = ttk.Frame(
            self.frame_status,
            style="Panel.TFrame"
        )

        self.frame_runtime = ttk.Frame(
            self.frame_status,
            style="Panel.TFrame"
        )

        # HEADER
        title = tk.Label(
            self.frame_status_header,
            text="STATUS DO GENSHIN",
            font=self.FONT_TITLE,
            fg=self.COLOR_GOLD,
            bg=self.COLOR_PANEL
        )

        # STATUS ATUAL
        status_label = tk.Label(
            self.frame_current_status,
            text="Status atual:",
            font=self.FONT_SUBTITLE,
            fg=self.COLOR_TEXT,
            bg=self.COLOR_PANEL
        )

        self.status_label_info = tk.Label(
            self.frame_current_status,
            textvariable=self.status_info,
            font=self.FONT_NORMAL,
            fg=self.COLOR_GOLD,
            bg=self.COLOR_PANEL
        )

        # ÚLTIMA ABERTURA
        last_open_label = tk.Label(
            self.frame_last_open,
            text="Última abertura:",
            font=self.FONT_SUBTITLE,
            fg=self.COLOR_TEXT,
            bg=self.COLOR_PANEL
        )

        last_open_info = tk.Label(
            self.frame_last_open,
            textvariable=self.last_open_info,
            font=self.FONT_NORMAL,
            fg=self.COLOR_MUTED,
            bg=self.COLOR_PANEL,
            wraplength=270
        )

        # TEMPO DE EXECUÇÃO
        runtime_label = tk.Label(
            self.frame_runtime,
            text="Tempo de execução:",
            font=self.FONT_SUBTITLE,
            fg=self.COLOR_TEXT,
            bg=self.COLOR_PANEL
        )

        self.runtime_label_info = tk.Label(
            self.frame_runtime,
            textvariable=self.runtime_info,
            font=("Segoe UI", 18, "bold"),
            fg=self.COLOR_BLUE,
            bg=self.COLOR_PANEL
        )

        # PACK
        title.pack()

        status_label.pack()
        self.status_label_info.pack(pady=(5, 0))

        last_open_label.pack()
        last_open_info.pack(pady=(5, 0))

        runtime_label.pack()
        self.runtime_label_info.pack(pady=(5, 0))

        self.frame_status_header.pack(pady=(15, 35))
        self.frame_current_status.pack(pady=10)
        self.frame_last_open.pack(pady=30)
        self.frame_runtime.pack(pady=20)

    # ======================================================
    # CONFIGURAÇÕES
    # ======================================================

    def create_config(self):

        # STRINGVAR
        self.start_with_windows_var = tk.BooleanVar(
            value=self.config["start_with_windows"]
        )

        self.toggle_notifications_var = tk.BooleanVar(
            value=self.config["toggle_notifications"]
        )

        self.interval_var = tk.StringVar(
            value=str(self.config["interval"])
        )

        self.delay_var = tk.StringVar(
            value=str(self.config["delay"])
        )

        # FRAMES
        self.frame_config_header = ttk.Frame(
            self.frame_config,
            style="Panel.TFrame"
        )

        self.frame_preferences = ttk.Frame(
            self.frame_config,
            style="Panel.TFrame"
        )

        self.frame_monitoring = ttk.Frame(
            self.frame_config,
            style="Panel.TFrame"
        )

        self.frame_config_button = ttk.Frame(
            self.frame_config,
            style="Panel.TFrame"
        )

        # HEADER
        title = tk.Label(
            self.frame_config_header,
            text="CONFIGURAÇÕES",
            font=self.FONT_TITLE,
            fg=self.COLOR_GOLD,
            bg=self.COLOR_PANEL
        )

        # PREFERÊNCIAS
        preferences_label = tk.Label(
            self.frame_preferences,
            text="Preferências",
            font=self.FONT_SUBTITLE,
            fg=self.COLOR_GOLD,
            bg=self.COLOR_PANEL
        )

        self.start_with_windows = tk.Checkbutton(
            self.frame_preferences,
            text="Iniciar com Windows",
            font=self.FONT_NORMAL,
            variable=self.start_with_windows_var,
            fg=self.COLOR_TEXT,
            bg=self.COLOR_PANEL,
            activebackground=self.COLOR_PANEL,
            activeforeground=self.COLOR_GOLD,
            selectcolor=self.COLOR_INPUT,
            highlightthickness=0,
            bd=0
        )

        self.toggle_notifications = tk.Checkbutton(
            self.frame_preferences,
            text="Ativar notificações",
            font=self.FONT_NORMAL,
            variable=self.toggle_notifications_var,
            fg=self.COLOR_TEXT,
            bg=self.COLOR_PANEL,
            activebackground=self.COLOR_PANEL,
            activeforeground=self.COLOR_GOLD,
            selectcolor=self.COLOR_INPUT,
            highlightthickness=0,
            bd=0
        )

        # MONITORAMENTO
        monitoring_label = tk.Label(
            self.frame_monitoring,
            text="Monitoramento",
            font=self.FONT_SUBTITLE,
            fg=self.COLOR_GOLD,
            bg=self.COLOR_PANEL
        )

        check_interval_label = tk.Label(
            self.frame_monitoring,
            text="Intervalo de verificação:",
            font=self.FONT_NORMAL,
            fg=self.COLOR_TEXT,
            bg=self.COLOR_PANEL
        )

        self.interval_entry = tk.Entry(
            self.frame_monitoring,
            textvariable=self.interval_var,
            font=self.FONT_NORMAL,
            width=12,
            justify="center",
            bg=self.COLOR_INPUT,
            fg=self.COLOR_TEXT,
            insertbackground=self.COLOR_TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_MUTED,
            highlightcolor=self.COLOR_GOLD
        )

        warning_interval_label = tk.Label(
            self.frame_monitoring,
            text="Mínimo: 1 segundo",
            font=self.FONT_SMALL,
            fg=self.COLOR_MUTED,
            bg=self.COLOR_PANEL
        )

        delay_label = tk.Label(
            self.frame_monitoring,
            text="Atraso para encerrar:",
            font=self.FONT_NORMAL,
            fg=self.COLOR_TEXT,
            bg=self.COLOR_PANEL
        )

        self.delay_to_close = tk.Entry(
            self.frame_monitoring,
            textvariable=self.delay_var,
            font=self.FONT_NORMAL,
            width=12,
            justify="center",
            bg=self.COLOR_INPUT,
            fg=self.COLOR_TEXT,
            insertbackground=self.COLOR_TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_MUTED,
            highlightcolor=self.COLOR_GOLD
        )

        warning_delay_label = tk.Label(
            self.frame_monitoring,
            text="Mínimo: 30 segundos",
            font=self.FONT_SMALL,
            fg=self.COLOR_MUTED,
            bg=self.COLOR_PANEL
        )

        # BOTÃO
        self.apply_config = tk.Button(
            self.frame_config_button,
            text="SALVAR CONFIGURAÇÕES",
            font=("Segoe UI", 10, "bold"),
            width=27,
            command=self.save_settings,
            bg=self.COLOR_GOLD,
            fg=self.COLOR_BG,
            activebackground="#E9CB8C",
            activeforeground=self.COLOR_BG,
            relief="flat",
            cursor="hand2",
            bd=0,
            pady=8
        )

        # PACK DOS ELEMENTOS
        title.pack()

        preferences_label.pack(pady=(0, 5))
        self.start_with_windows.pack(anchor="w", pady=1)
        self.toggle_notifications.pack(anchor="w", pady=1)

        monitoring_label.pack(pady=(0, 5))

        check_interval_label.pack()
        self.interval_entry.pack(pady=(3, 2))
        warning_interval_label.pack(pady=(0, 5))

        delay_label.pack()
        self.delay_to_close.pack(pady=(3, 2))
        warning_delay_label.pack()

        self.apply_config.pack()


        # PACK DOS FRAMES
        self.frame_config_header.pack(pady=(5, 10))
        self.frame_preferences.pack(pady=(5, 8))
        self.frame_monitoring.pack(pady=3)
        self.frame_config_button.pack(pady=(12, 5))

    # ======================================================
    # SALVAR CONFIGURAÇÕES
    # ======================================================

    def save_settings(self):
        if self.validate_config():

            current_settings = {
                "start_with_windows": self.start_with_windows_var.get(),
                "toggle_notifications": self.toggle_notifications_var.get(),
                "interval": int(self.interval_var.get()),
                "delay": int(self.delay_var.get())
            }

            self.config.update(current_settings)
            config_manager.save_config(self.config)

            if current_settings["start_with_windows"]:
                startup.enable_startup()
            else:
                startup.disable_startup()

            messagebox.showinfo(
                "Sucesso",
                "Configurações salvas com sucesso!",
                parent=self.window
            )

        else:
            messagebox.showerror(
                "Erro",
                "Verifique os valores informados:\n\n"
                "Intervalo mínimo: 1 segundo.\n"
                "Delay mínimo: 30 segundos.",
                parent=self.window
            )

    # ======================================================
    # VALIDAÇÃO
    # ======================================================

    def validate_config(self):

        interval = self.interval_var.get()
        delay = self.delay_var.get()

        success = []

        if interval.isdigit():
            interval = int(interval)

            if interval > 0:
                success.append("Interval Okay!")

        if delay.isdigit():
            delay = int(delay)

            if delay >= 30:
                success.append("Delay Okay!")

        return len(success) == 2

    # ======================================================
    # JANELA
    # ======================================================

    def start(self):
        self.window.mainloop()

    def hide_window(self):
        self.window.withdraw()

    def show_window(self):
        self.window.deiconify()

    # ======================================================
    # ATUALIZAR STATUS
    # ======================================================

    def update_status(self, status, last_open, runtime):

        if status == "Aberto":
            color = self.COLOR_GREEN

        elif status == "Fechado":
            color = self.COLOR_RED

        else:
            color = self.COLOR_GOLD

        self.window.after(
            0,
            lambda: (
                self.status_info.set(status),
                self.last_open_info.set(last_open),
                self.runtime_info.set(runtime),
                self.status_label_info.config(fg=color)
            )
        )


if __name__ == "__main__":
    app = Interface(config_manager.load_config())
    app.start()
