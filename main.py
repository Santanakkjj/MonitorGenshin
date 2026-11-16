import os
import sys
import threading

import pystray
from PIL import Image

import config_manager
from interface import Interface
from monitor import monitor_genshin

# ==================================================
# CONFIGURAÇÕES INICIAIS
# ==================================================

stop_event = threading.Event()
config = config_manager.load_config()

interface = Interface(config=config)
interface.hide_window()


# ==================================================
# LOCALIZAÇÃO DOS ARQUIVOS
# ==================================================

def get_icon_path():
    base_dir = getattr(
        sys,
        "_MEIPASS",
        os.path.dirname(os.path.abspath(__file__))
    )

    return os.path.join(base_dir, "assets", "icone.png")


icon_path = get_icon_path()
image = Image.open(icon_path)


# ==================================================
# MENU DA BANDEJA
# ==================================================

def exit_monitor(icon, item):
    stop_event.set()
    icon.stop()

    interface.window.after(
        0,
        interface.window.destroy
    )

    monitor_thread.join(timeout=5)


def open_interface(icon, item):
    interface.window.after(
        0,
        interface.show_window
    )


def create_tray_menu():
    return pystray.Menu(
        pystray.MenuItem("Abrir", open_interface, default=True),
        pystray.MenuItem("Sair", exit_monitor)
    )


# ==================================================
# ÍCONE DA BANDEJA
# ==================================================

icon = pystray.Icon(
    "GenshinMonitor",
    image,
    "Monitor do Genshin",
    menu=create_tray_menu()
)


# ==================================================
# THREADS
# ==================================================

monitor_thread = threading.Thread(
    target=monitor_genshin,
    args=(
        stop_event, 
        icon_path, 
        config, 
        interface.update_status
    ),
    daemon=True
)

tray_thread = threading.Thread(
    target=icon.run,
    daemon=True
)


def start_threads():
    monitor_thread.start()
    tray_thread.start()


# ==================================================
# EXECUÇÃO PRINCIPAL
# ==================================================

def main():
    start_threads()
    interface.window.mainloop()


if __name__ == "__main__":
    main()
