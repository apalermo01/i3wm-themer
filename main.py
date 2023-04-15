from i3wmthemer.models import colors
from i3wmthemer.models import i3
import json

def main():
    path = "./themes/trees/trees.json"
    with open(path, "r") as f:
        config = json.load(f)

    config = colors.parse_colors(config)
    i3.parse_i3theme(configuration_data=config)
if __name__ == '__main__':
    main()
