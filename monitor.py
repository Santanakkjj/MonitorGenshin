from datetime import datetime
from time import time

import psutil
import pygetwindow as gw

import config_manager
from notifications import notify

# ==================================================
# ENCERRAMENTO DE PROCESSOS
# ==================================================

def terminate_process(proc):
    try:
        proc.terminate()
        proc.wait(timeout=3)

    except psutil.TimeoutExpired:
        try:
            proc.kill()
            proc.wait(timeout=3)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.TimeoutExpired
        ):
            pass

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied
    ):
        pass


# ==================================================
# CONTROLE DE PROCESSOS
# ==================================================

def close_genshin(proc, pid, process_start_times, icon_path, notifications):
    terminate_process(proc)

    notify(icon_path, notifications)
    process_start_times.pop(pid, None)


# ==================================================
# MONITORAMENTO
# ==================================================

def monitor_genshin(stop_event, icon_path, config, update_callback):

    process_start_times = {}
    window_was_open = False
    monitor_start_time = time()

    last_open = config.get("last_open") or "Nenhuma abertura registrada."
    runtime_start = None

    while not stop_event.is_set():

        # CONFIGURAÇÕES
        interval = config["interval"]
        delay = config["delay"]

        notifications = config["toggle_notifications"]

        # DETECÇÃO DA JANELA
        genshin_window = gw.getWindowsWithTitle("Genshin Impact")
        genshin_process_found = False

        if genshin_window:
            if not window_was_open:
                last_open_time = time()
                runtime_start = time()

                last_open = datetime.fromtimestamp(
                    last_open_time
                ).strftime("%d/%m/%Y às %H:%M:%S")

                config_manager.save_last_open(last_open)

            window_was_open = True

        if genshin_window and runtime_start:
            elapsed = time() - runtime_start

            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)

            runtime = f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            runtime = "--:--:--"

        status = "Aberto" if genshin_window else "Fechado"

        update_callback(
            status,
            last_open,
            runtime
        )

        # PERCORRE OS PROCESSOS
        for proc in psutil.process_iter(["pid", "name"]):

            try:
                if proc.info["name"] != "GenshinImpact.exe":
                    continue

                genshin_process_found = True

                pid = proc.info["pid"]
                process_created = proc.create_time()

                # VERIFICA SE O PROCESSO JÁ ESTAVA ABERTO ANTES DO MONITORAMENTO
                if process_created < monitor_start_time and not genshin_window:

                    close_genshin(
                        proc, pid, process_start_times, icon_path, notifications
                    )

                    continue

                # SE O JOGO JÁ FOI ABERTO E SUA JANELA FOI FECHADA
                if window_was_open and not genshin_window:

                    close_genshin(
                        proc, pid, process_start_times, icon_path, notifications
                    )

                    continue

                # REGISTRA O TEMPO DE DETECÇÃO
                if pid not in process_start_times:
                    process_start_times[pid] = time()

                elapsed_time = time() - process_start_times[pid]

                # TEMPO LIMITE PARA ABERTURA DA JANELA
                if not window_was_open and elapsed_time >= delay:

                    close_genshin(
                        proc, pid, process_start_times, icon_path, notifications
                    )

                    continue

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.TimeoutExpired
            ):
                continue

        # REINICIA O ESTADO QUANDO O PROCESSO NÃO EXISTE
        if not genshin_process_found:
            process_start_times.clear()
            window_was_open = False

        # AGUARDA O PRÓXIMO CICLO
        stop_event.wait(interval)
