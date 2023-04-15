from i3wmthemer.models.colors import parse_colors
import json

if __name__ == '__main__':

    path = "./themes/000/000.json"
    with open(path, "r") as f:
        config = json.load(f)
    parse_colors(config['colors'])
