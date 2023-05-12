from i3wmthemer.models import colors
from i3wmthemer.models import i3
from i3wmthemer.models import polybar
from i3wmthemer.models import vim
from i3wmthemer.models import bash
from i3wmthemer.models import wallpaper
from i3wmthemer.models import picom
import json
import os
import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def main():
    theme_name = 'trees'
    path = "./themes/trees/trees.json"
    with open(path, "r") as f:
        config = json.load(f)

    config = colors.parse_colors(config)
    wallpaper.parse_wallpaper(config)
    i3.parse_i3theme(config=config,
                    write_path=os.path.expanduser("~/.config/i3/config"),
                    theme_name = theme_name)
    polybar.parse_polybar(config,
                          write_path=os.path.expanduser("~/.config/polybar/config.ini"),
                          theme_name=theme_name)
    vim.parse_vim(config=config, write_path=os.path.expanduser("~/.vimrc"), theme_name=theme_name)
    bash.parse_bash(config=config, write_path=os.path.expanduser("~/.bashrc"))
    picom.parse_picom(config=config, write_path = os.path.expanduser("~/.config/picom.conf"), theme_name=theme_name)
if __name__ == '__main__':
    main()
