import configparser
import os
import shutil
from typing import Dict
import logging

logger = logging.getLogger(__name__)

def parse_polybar(config: Dict,
                  write_path: str,
                  theme_name: str):

    # get settings
    polybar_config = config['polybar']

    # load the theme-specific polybar config
    polybar = configparser.ConfigParser()
    read_path = f"./themes/{theme_name}/polybar.ini"
    if not os.path.exists(read_path):
        polybar.read(f"./defaults/polybar.template")
    else:
        polybar.read(f"./themes/{theme_name}/polybar.ini")

    # add colors from the pallet
    if 'colors' not in polybar:
        polybar['colors'] = {}
    for c in config['colors']['pallet']:
        polybar['colors'][c] = config['colors']['pallet'][c]
    if 'colors' in config['polybar']:
        for c in config['polybar']['colors']:
            polybar['colors'][c] = config['polybar']['colors'][c]
    # polybar['colors'] = config['colors']['pallet']
    polybar = init_modules(config, polybar)
    polybar = parse_includes(config, polybar, theme_name)
    polybar = parse_opts(config, polybar)

    with open(write_path, "w") as f:
        polybar.write(f)

    # launch script
    src_script = "./scripts/i3wmthemer_bar_launch.sh"
    dest = "/" + os.path.join(*write_path.split('/')[:-1])
    dest_script = os.path.join(dest, "i3wmthemer_bar_launch.sh")
    if not os.path.exists(dest):
        os.makedirs(dest)
    with open(dest_script, 'w') as f:
        pass
    shutil.copy2(src_script, dest)
    return config
def init_modules(config, polybar):
    for module in config['polybar']:
        if '/' in module:
            if module not in polybar:
                polybar[module] = {}
    return polybar

def parse_includes(config, polybar, theme_name):
    for key in config['polybar']:
        if "/" in key and "include" in config['polybar'][key]:
            include_path = config['polybar'][key]['include']

            # relative path from project source
            if include_path[0] == '.':
                path = os.path.abspath(include_path)
                logger.info(f"using relative path - pulling module {key} from {path}")
            # module file lives in theme directory
            else:
                path = os.path.abspath(os.path.join('.', 'themes', theme_name, include_path))
                logger.info(f"using theme path - pulling module {key} from {path}")
            polybar[key]['include-file'] = path

    return polybar

def parse_opts(config, polybar):
    for key in config['polybar']:
        if '/' in key:
            for option in config['polybar'][key]:
                if option != 'include':
                    polybar[key][option] = config['polybar'][key][option]
    return polybar
