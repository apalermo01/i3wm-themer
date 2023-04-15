import logging
from typing import Union, Dict, List
import subprocess

logger = logging.getLogger(__name__)

def parse_colors(#template: Dict,
                 config: Dict):
    """parse_colors.

    :param config:
    :type config: Dict
    """
    """
    parse color info in 2 modes depending on config.

    v1:
    - 2 options for color mode: manually specify palett or use pywal
        {'color_mode': 'pywal',
         'image_name': 'wallpaper.png',
         'pywal_args': {}
         }

        {'color_mode': 'manual'}

    - define a template for colorscheme
        this will likely be similar to the xresources colors
    """

    if config is None or config['colors']['settings']['color_mode'] == 'pywal':
        wallpaper = config['wallpaper']
        pallet = configure_pywal_colors(config['settings'], config['wallpaper'])
        config['colors']['pallet'] = pallet

    return config


def configure_pywal_colors(settings, wallpaper_path):
    subprocess.run(['wal', '-n', '-e', '-i', wallpaper_path], capture_output=True)

    with open("~/.cache/wal/colors.json", "r") as f:
        pywal_colors = json.load(f)

    pallet = {}
    for s in pywal_colors['special']:
        pallet[s] = pywal_colors['special'][s]
    for c in pywal_colors['colors']:
        pallet[c] = pywal_colors['colors'][c]
    return pallet
