from typing import Dict, IO, List
import os
import shutil
import logging

logger = logging.getLogger(__name__)

def parse_vim(config: Dict,
              write_path: str,
              theme_name: str,
              backup = False):

    logger.info("starting to parse vimrc")
    vim_config = config.get('vim', {})

    colors = vim_config.get('colors', 'gruvbox')
    colorscheme = vim_config.get('colorscheme', 'gruvbox')
    airline_theme  = vim_config.get('airline_theme', 'dark')
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
        logger.info("end extra lines for vim")

    # write to the tempfile
    with open("./defaults/vimrc.template", "r") as f_template,\
        open("./tmp/.vimrc", "w") as f_temp:

        write_tempfile(f_template,
                       f_temp,
                       colors,
                       colorscheme,
                       airline_theme,
                       plugs,
                       extra_lines)
    # handle colors
    if colors != 'gruvbox':
        colors_path = f"./themes/{theme_name}/{colors}"

        if 'vim' not in write_path:
            colors_dest = os.path.expanduser(f"~/.vim/colors/{colors}")
        else:
            colors_dest = os.path.expanduser(f"~/.config/nvim/colors/{colors}")
        shutil.copy(src=colors_path, dst=colors_dest)
        logger.info(f"copied colors script from {colors_path} to {colors_dest}")


    # write to file
    # shutil.copy(src="./tmp/.vimrc", dst=os.path.expanduser("~/.vimrc"))
    shutil.copy(src="./tmp/.vimrc", dst=write_path)
    logger.info("wrote vimrc to file")
    return config

def write_tempfile(f_template: IO,
                   f_temp: IO,
                   colors: str,
                   colorscheme: str,
                   airline_theme: str,
                   plugs: List,
                   extra_lines: List):

    # write the base file
    for line in f_template.readlines():

        # check if we're in the plug section
        if "call plug#begin(" in line:
            f_temp.write(line)
            for p in plugs:
                f_temp.write(f"Plug '{p}'\n")

        elif len(line) >= len('colorscheme') and line[:len('colorscheme')] == 'colorscheme':
            f_temp.write(f'colorscheme {colorscheme}\n')
        elif len(line) >= len('let g:airline_theme=') and line[:len('let g:airline_theme=')] == 'let g:airline_theme=':
            f_temp.write(f'let g:airline_theme="{airline_theme}"\n')
        else:
            # write normal line
            f_temp.write(line)


