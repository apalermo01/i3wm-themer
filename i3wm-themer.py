#!/bin/env python3

"""
i3-wm theme changing utility.

Author  :   Stavros Grigoriou (@unix121), modified by Alex Palermo (@apalermo01)
"""
from i3wmthemer.models.colors import parse_colors
from i3wmthemer.models.i3 import parse_i3theme
from i3wmthemer.models.polybar import parse_polybar
import logging
import sys
import json
import os

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

logger = logging.getLogger(__name__)

func_registry = {
    'colors': {
        'function': parse_colors,
        'write_path': ""},
    'i3': {
        'function': parse_i3theme,
        'write_path': "./test/i3.config"},
    'polybar': {
        'function': parse_polybar,
        'write_path': "./test/polybar.ini"
    }
}

theme_path = "./themes/"
def test_main():
    theme = 'trees'
    with open(os.path.join(theme_path, theme, f"{theme}.json"), "r") as f:
        theme_config = json.load(f)

    print(theme_config)
    keys = list(theme_config.keys())

    for k in keys:
        if k not in ['colors', 'i3']:
            continue
        theme_config = func_registry[k]['function'](config=theme_config,
                write_path=func_registry[k]['write_path'])

if __name__ == "__main__":
    test_main()
