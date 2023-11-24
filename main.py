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
logger = logging.getLogger(__name__)

path_config = {
        'colors': None,
        'wallpaper': None,
        'i3wm': os.path.expanduser("~/.config/i3/config"),
        'polybar': os.path.expanduser("~/.config/polybar/config.ini"),
        'vim': os.path.expanduser("~/.vimrc"),
        'bash': os.path.expanduser("~/.bashrc"),
        'picom': os.path.expanduser("~/.config/picom.conf"),
        }

func_registry = {
    'colors': colors.parse_colors,
    'wallpaper': wallpaper.parse_wallpaper,
    'i3wm': i3.parse_i3theme,
    'polybar': polybar.parse_polybar,
    'vim': vim.parse_vim,
    'bash': bash.parse_bash,
    'picom': picom.parse_picom,
}

order = ['colors', 'wallpaper', 'i3wm', 'polybar', 'vim', 'bash', 'picom']
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme")
    parser.add_argument("--backup", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    theme_name = args.theme
    path = f"./themes/{theme_name}/{theme_name}.json"

    with open(path, "r") as f:
        config = json.load(f)

    backup = False

    for key in order:
        if key in config:
            logger.info(f"parsing {key}")
            config = func_registry[key](
                    config=config,
                    write_path=path_config[key],
                    theme_name=theme_name,
                    backup=backup)

if __name__ == '__main__':
    main()
