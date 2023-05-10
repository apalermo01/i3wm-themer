from typing import Dict, IO, List
import os
import shutil


def parse_vim(config: Dict,
              write_path: str,
              theme_name: str):
    # TODO: don't hardcode save paths
    vim_config = config['vim']

    colors = vim_config.get('colors', 'gruvbox')
    colorscheme = vim_config.get('colorscheme', 'gruvbox')
    plugs = vim_config.get('plugs', [])
    extra_lines = vim_config.get('extra_lines', [])

    # write to the tempfile
    with open("./defualts/vimrc.template", "r") as f_template,\
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
        shutil.copy(src=colors_path, dst=os.path.expanduser("~/.vim/colors/"))

    with open("./tmp/.vimrc", "a") as f:
        f.write(f"colorschemes {colorscheme}")

    # write to file
    shutil.copy(src="./tmp/.vimrc", dst=os.path.expanduser("~/.vimrc"))

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
