from i3wmthemer.models import colors

import json

def main():
    path = "./themes/trees/trees.json"
    with open(path, "r") as f:
        config = json.load(f)

    config = colors.parse_colors(config)

if __name__ == '__main__':
    main()
