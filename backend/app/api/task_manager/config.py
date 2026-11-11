import tomllib

from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.toml"

def load_config():
    with open(CONFIG_PATH, "rb") as file:
        return tomllib.load(file)

