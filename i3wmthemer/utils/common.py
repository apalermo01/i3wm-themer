import json
from datetime import datetime

def get_colors_from_wal():
    path = "~/.cache/wal/colors.json"
    with open(path, "r") as f:
        colors_dict = json.load(f)

    return colors_dict

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d:%H:%M%S")
