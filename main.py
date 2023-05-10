from i3wmthemer.models import colors
from i3wmthemer.models import i3
from i3wmthemer.models import polybar
from i3wmthemer.models import vim
from i3wmthemer.models import bash
import json
import os


def main():
    theme_name = 'trees'
    path = "./themes/trees/trees.json"
    with open(path, "r") as f:
        config = json.load(f)

    config = colors.parse_colors(config)
    i3.parse_i3theme(config=config, write_path=os.path.expanduser("~/.config/config"))
    polybar.parse_polybar(config, write_path=os.path.expanduser("~/.config/polybar/config.ini"))
    vim.parse_vim(config=config, write_path=os.path.expanduser("~/.vimrc"), theme_name=theme_name)
if __name__ == '__main__':
    main()
