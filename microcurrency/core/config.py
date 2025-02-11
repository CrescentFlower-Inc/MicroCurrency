from pathlib import Path
import json5

conffile = Path(__file__).parents[2] / "config.json5"

def get_config():
    with open(conffile) as f:
        return json5.loads(f.read())