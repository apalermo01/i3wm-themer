import logging
from typing import Union, Dict, List
import os
import json
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import json

logger = logging.getLogger(__name__)

def parse_colors(#template: Dict,
                 config: Dict,
                 write_path: str = None):
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

    if config is None or ('settings' in config['colors'] and config['colors']['settings']['color_mode'] == 'pywal'):
        wallpaper = config['wallpaper']
        pallet = configure_pywal_colors(config['wallpaper'])
        logger.debug(f"pallet derived from pywal")
        config['colors']['pallet'] = pallet
    else:

        # remove rofi colors (used in default configs)
        pallet_new = {}
        for p in config['colors']['pallet']:
            if 'rofi' not in p:
                pallet_new[p] = config['colors']['pallet'][p]
        config['colors']['pallet'] = pallet_new
        pallet = config['colors']['pallet']

        logger.debug("using manual pallet")
    if 'black' not in config['colors']['pallet']:
        config['colors']['pallet']['black'] = "#000000"
    make_pallet_image(pallet)
    with open("./tmp/pallet.json", "w") as f:
        json.dump(pallet, f, indent=2)
    return config


def configure_pywal_colors(wallpaper_path):
    subprocess.run(['wal', '-n', '-e', '-i', wallpaper_path], capture_output=False)
    logger.debug(f"ran pywal on {wallpaper_path}")
    colors_file = os.path.expanduser("~/.cache/wal/colors.json")
    with open(colors_file, "r") as f:
        pywal_colors = json.load(f)
    logger.debug(f"colors file: {json.dumps(pywal_colors, indent=2)}")
    pallet = {}
    for s in pywal_colors['special']:
        pallet[s] = pywal_colors['special'][s]
    for c in pywal_colors['colors']:
        pallet[c] = pywal_colors['colors'][c]
    logger.debug("pallet configuration successful")
    return pallet


def make_pallet_image(pallet):
    total_colors = len(pallet)
    nrows = (total_colors+1) // 2
    ncols = 2
    colors_list = list(pallet.values())
    titles = list(pallet.keys())
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6, 2*nrows))
    axes = axes.flatten()
    for i, color in enumerate(colors_list):
        axes[i].set_facecolor(color)
        axes[i].xaxis.set_visible(False)
        axes[i].yaxis.set_visible(False)
        axes[i].set_title(f"{titles[i]}: {color}")
    fig.suptitle("Color Palette", fontsize=14)
    # ax.set_yticks(range(len(colors_list)))
    # ax.set_yticklabels(list(pallet.keys()))
    # ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

    # ax.set_title("pallet")
    plt.savefig("./tmp/pallet.png", dpi=300, bbox_inches='tight')
