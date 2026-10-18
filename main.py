import os
import sys
import threading
from time import time

import psutil
import pygetwindow as gw
import pystray
from PIL import Image
from winotify import Notification

stop_event = threading.Event()
process_start_times = {}  
window_was_open = False 

def notify():
    notification = Notification(
        app_id="Monitor do Genshin",
        title="Monitor do Genshin",
        msg="O Genshin impact foi encerrado automaticamente.",
        icon=icon_path
    )
    notification.show()

def monitor_genshin():
    global window_was_open

    while not stop_event.is_set():

        genshin_window = gw.getWindowsWithTitle("Genshin Impact")  # obs: se o nome da janela não coincidir pode ser um problema futuramente
        genshin_process_found = False  

        if genshin_window:
            window_was_open = True  


        # PERCORRE TODOS OS PROCESSOS EM EXECUÇÃO PROCURANDO PELO GENSHIN
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"] != "GenshinImpact.exe":
                    continue

                print("Processo do Genshin encontrado!")
                genshin_process_found = True
                pid = proc.info["pid"]  # PEGA O ID DO PROCESSO DO GENSHIN

                 # SE A JANELA DO GENSHIN JÁ ABRIU ANTES E AGORA ESTÁ FECHADA, ENCERRA O PROCESSO DO GENSHIN
                if window_was_open and not genshin_window:
                    try:
                        proc.terminate()
                        proc.wait(timeout=3)

                    except psutil.TimeoutExpired:
                        try:
                            proc.kill()
                            proc.wait(timeout=3)
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                            pass

                    except psutil.NoSuchProcess:
                        pass

                    except psutil.AccessDenied:
                        pass

                    notify()
                    process_start_times.pop(pid, None)
                    continue

                # REGISTRA QUANDO O PROCESSO FOI DETECTADO PELA PRIMEIRA VEZ
                if pid not in process_start_times:
                    process_start_times[pid] = time()

                elapsed_time = time() - process_start_times[pid]  # CALCULA QUANTO TEMPO PASSOU


                # SE A JANELA DO GENSHIN NÃO ABRIR EM 60 SEGUNDOS, TENTA ENCERRAR O PROCESSO
                # obs: necessário pois sem isso não era possível iniciar o jogo já que o processo abria antes da janela aparecer

                if not window_was_open and elapsed_time >= 60:
                    proc.terminate()  
                    proc.wait(timeout=3)  
                    notify()
                    process_start_times.pop(pid, None)

            # IGNORA PROCESSOS QUE JÁ FECHARAM, QUE NÃO TEM PERMISSAO OU QUE NÃO ENCERRARAM A TEMPO
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.TimeoutExpired
            ):
                continue

    
        if not genshin_process_found:
            process_start_times.clear()
            window_was_open = False

        stop_event.wait(5)  # ESPERA 5 SEGUNDOS OU ATÉ O MONITOR SER ENCERRADO

def exit_monitor(icon, item):
    stop_event.set()
    icon.stop()



base_dir = getattr(
    sys, "_MEIPASS",
    os.path.dirname(os.path.abspath(__file__))
)

icon_path = os.path.join(base_dir, "icone.png")
image = Image.open(icon_path)


menu = pystray.Menu(
    pystray.MenuItem("Sair", exit_monitor)
)


icon = pystray.Icon(
    "GenshinMonitor",
    image,
    "Monitor do Genshin",
    menu=menu
)


monitor_thread = threading.Thread(
    target=monitor_genshin,
    daemon=True
)
monitor_thread.start()


icon.run()


stop_event.set()
monitor_thread.join(timeout=5)
