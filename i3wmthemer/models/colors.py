import logging
from typing import Union, Dict, List

logger = logging.getLogger(__name__)

def parse_colors(template: Dict,
                 config: Dict):
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
