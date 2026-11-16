import json

DEFAULT_CONFIG = {
    "start_with_windows": False,
    "toggle_notifications": True,
    "interval": 5,
    "delay": 60,
    "last_open": None
}

def save_config(config):
    with open("config.json", "w") as arquivo:
        json.dump(config, arquivo, indent=4, ensure_ascii=False)

def load_config():
    try:
        with open("config.json", "r") as arquivo:
            config = json.load(arquivo)

    except FileNotFoundError:
        config = DEFAULT_CONFIG.copy()

    for key, value in DEFAULT_CONFIG.items():
        config.setdefault(key, value)

    save_config(config)

    return config

def save_last_open(last_open):
    config = load_config()
    config["last_open"] = last_open
    save_config(config)