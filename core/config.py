import json

CONFIG_FILE = "core/config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def set_theme(theme):
    config = load_config()
    config["theme"] = theme
    save_config(config)

def get_theme():
    return load_config().get("theme", "rainbow")