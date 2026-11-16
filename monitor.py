
from datetime import datetime
from time import time

import psutil
import pygetwindow as gw

import config_manager
from notifications import notify


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


def close_genshin(proc, pid, process_start_times, icon_path, notifications):
    terminate_process(proc)
    notify(icon_path, notifications)
    process_start_times.pop(pid, None)


def monitor_genshin(stop_event, icon_path, config, update_callback):

    process_start_times = {}
    game_was_running = False
    window_was_open = False

    last_open = config.get("last_open") or "Nenhuma abertura registrada."

    while not stop_event.is_set():

        interval = config["interval"]
        delay = config["delay"]
        notifications = config["toggle_notifications"]

        genshin_window = [
            window
            for window in gw.getWindowsWithTitle("Genshin Impact")
            if window.title == "Genshin Impact"
        ]
        
        window_found = bool(genshin_window)

        genshin_proc = None

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"] == "GenshinImpact.exe":
                    genshin_proc = proc
                    break

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        runtime = "--:--:--"

        if genshin_proc is not None:

            pid = genshin_proc.info["pid"]
            process_created = genshin_proc.create_time()

            if pid not in process_start_times:
                process_start_times[pid] = time()

            # JOGO ABERTO
            if window_found:

                if not window_was_open:

                    last_open = datetime.fromtimestamp(
                        process_created
                    ).strftime("%d/%m/%Y às %H:%M:%S")

                    config_manager.save_last_open(last_open)

                window_was_open = True
                game_was_running = True

                elapsed = time() - process_created

                hours = int(elapsed // 3600)
                minutes = int((elapsed % 3600) // 60)
                seconds = int(elapsed % 60)

                runtime = f"{hours:02}:{minutes:02}:{seconds:02}"

            # PROCESSO SEM JANELA DEPOIS DE O JOGO TER ABERTO
            elif game_was_running:

                close_genshin(
                    genshin_proc,
                    pid,
                    process_start_times,
                    icon_path,
                    notifications
                )

                process_start_times.clear()
                game_was_running = False
                window_was_open = False

            # PROCESSO AINDA INICIANDO
            else:

                elapsed = time() - process_start_times[pid]

                if elapsed >= delay:

                    close_genshin(
                        genshin_proc,
                        pid,
                        process_start_times,
                        icon_path,
                        notifications
                    )

                    process_start_times.clear()

        else:
            process_start_times.clear()
            game_was_running = False
            window_was_open = False

        status = "Aberto" if window_found and genshin_proc is not None else "Fechado"

        update_callback(status, last_open, runtime)

        stop_event.wait(interval)
