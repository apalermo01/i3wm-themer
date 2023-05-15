from typing import Dict, IO, List
import os
import shutil
import logging

logger = logging.getLogger(__name__)

def parse_vim(config: Dict,
              write_path: str,
              theme_name: str):
    # TODO: don't hardcode save paths
    logger.info("starting to parse vimrc")
    vim_config = config.get('vim', {})

    colors = vim_config.get('colors', 'gruvbox')
    colorscheme = vim_config.get('colorscheme', 'gruvbox')
    plugs = vim_config.get('plugs', [])
    extra_lines = vim_config.get('extra_lines', [])

    logger.info(f"colors = {colors}")
    logger.info(f"colorscheme = {colorscheme}")
    if len(plugs) > 0:
        logger.info("Plugs:")
        for p in plugs:
            logger.info(p)
        logger.info("end vim plugs")
    if len(extra_lines) > 0:
        logger.info("extra lines for vimrc:")
        for l in extra_lines:
            logger.info(l)
        logger.ingo("end extra lines for vim")

    # write to the tempfile
    with open("./defaults/vimrc.template", "r") as f_template,\
        open("./tmp/.vimrc", "w") as f_temp:

        write_tempfile(f_template,
                       f_temp,
                       colors,
                       colorscheme,
                       plugs,
                       extra_lines)
    # handle colors
    if colors != 'gruvbox':
        colors_path = f"./themes/{theme_name}/{colors}"
        colors_dest = os.path.expanduser(f"~/.vim/colors/{colors}")
        shutil.copy(src=colors_path, dst=colors_dest)
        logger.info(f"copied colors script from {colors_path} to {colors_dest}")

    with open("./tmp/.vimrc", "a") as f:
        line = f"colorscheme {colorscheme}"
        f.write(line)
        logger.info(f"wrote {line} to .vimrc")

    # write to file
    shutil.copy(src="./tmp/.vimrc", dst=os.path.expanduser("~/.vimrc"))
    logger.info("wrote vimrc to file")

def write_tempfile(f_template: IO,
                   f_temp: IO,
                   colors: str,
                   colorscheme: str,
                   plugs: List,
                   extra_lines: List):

    # write the base file
    for line in f_template.readlines():

        # check if we're in the plug section
        if "call plug#begin(" in line:
            for p in plugs:
                f_temp.write(p)

        # write normal line
        f_temp.write(line)

    # 
