import os
from typing import Dict
import logging
from textwrap import dedent
import shutil


logger = logging.getLogger(__name__)


def parse_wallpaper(config: Dict):

    if isinstance(config['wallpaper'], str):
        name = config['wallpaper']
        config['wallpaper'] = {
                'method': 'feh',
                'name': name}

    method = config['wallpaper']['method']

    if method == 'feh':
        config = feh_theme(config)
    else:
        raise NotImplementedError
    return config

def feh_theme(config: Dict):

    wallpaper_path = config['wallpaper']['name']
    if not os.path.exists(os.path.expanduser("~/Pictures/wallpapers/")):
        os.makedirs(os.path.expanduser("~/Picutres/wallpapers/"))
    logger.warning("Loading wallpaper")

    # TODO: move this functionality to the i3 module
    if 'extra_lines' not in config['i3']:
        config['i3']['extra_lines'] = []

    config['i3']['extra_lines'].append(dedent(f"""
        \nexec_always feh --bg-fill $HOME/Pictures/wallpapers/{wallpaper_path.split("/")[-1]}
        """))
    shutil.copy2(src=wallpaper_path,
                 dst=os.path.expanduser(f"~/Pictures/wallpapers/{wallpaper_path.split('/')[-1]}"))


    return config

