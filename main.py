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
import argparse

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

path_config = {
        'colors': None,
        'wallpaper': None,
        'i3wm': os.path.expanduser("~/.config/i3/config"),
        'polybar': os.path.expanduser("~/.config/polybar/config.ini"),
        'vim': os.path.expanduser("~/.vimrc"),
        'bash': os.path.expanduser("~/.bashrc"),
        'picom': os.path.expanduser("~/.config/picom.conf"),
        }

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    theme_name = args.theme
    path = f"./themes/{theme_name}/{theme_name}.json"
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
    if 'bash' in config:
        bash.parse_bash(config=config, write_path=os.path.expanduser("~/.bashrc"))
    picom.parse_picom(config=config, write_path = os.path.expanduser("~/.config/picom.conf"), theme_name=theme_name)

if __name__ == '__main__':
    main()
