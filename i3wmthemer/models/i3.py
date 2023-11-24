import logging
from typing import Union, Dict, List
from i3wmthemer.fileutils import replace_line
import os
from i3wmthemer.utils.common import get_timestamp
import shutil

logger = logging.getLogger(__name__)


def check_total_lines():
    with open("./tmp/i3.config", "r") as f:
        total_lines = len([_ for _ in f.readlines()])
    logger.debug(f"{total_lines} lines in ./tmp/i3.config")

def read_tmp():
    with open("./tmp/i3.config", "r") as f:
        lines = f.readlines()
    return lines

def write_tmp(lines):
    with open("./tmp/i3.config", "w") as f:
        f.writelines(lines)

def parse_i3theme(config: Dict,
                  write_path: str,
                  theme_name: str,
                  default_path: str = "./defaults/",
                  backup: bool = False):
    """
    Configures i3wm settings from a base file

    :param config: main config file
    :param write_path: path that we should write the final output to
    :param theme_name: name of the current theme
    :param default_path: path to the default file

    Flow:
    1) loads key mappings from defaults
    2) loads base settings from defaults
    3) fills in colors
    4) configures terminal settings (e.g. default terminal, sets key command to open terminal
    5) adding bindsyms
    6) adds a list of extra lines found in the

    Each function writes to / modifies a file in a temp directory. Once everything is
    finished, that temp file is moved to the actual config file
    """
    # initialize tmep file
    if backup:
        i3_path = os.path.expanduser("~/.config/i3/")
        fname = f"i3_config_backup_{get_timestamp()}"
        shutil.copy2(src=os.path.join(i3_path, "config"), dst=os.path.join(i3_path, fname))

    with open("tmp/i3.config", "w") as f:
        logger.warning("overwrote i3.config temp file")

    # allow config to overwrite default file
    if 'default_path' in config['i3wm']:
        default_path = config['i3wm']['default_path']

    # load from template
    key_mappings(base_path=default_path)
    base_settings(base_path=default_path)

    # load from config
    write_colors(config=config)
    config_terminal(config=config)
    configure_bindsyms(config=config)
    configure_extra_lines(config=config)

    # append theme-specific lines
    configure_extend(config=config, theme_name=theme_name)

    # move config to final location
    with open("./tmp/i3.config", "r") as f_out, open(write_path, "w") as f_in:
        for r in f_out.readlines():
            f_in.write(r)
    return config

def key_mappings(base_path: str):
    """Writes the default keybindings to a temp file
    """
    logger.warning("about to write bindsyms to tmp file")
    with open(os.path.join(base_path, "i3_keybindings.template"), "r") as f:
        keybindings = f.readlines()

    with open("./tmp/i3.config", "a") as f:
        f.writelines(keybindings)

    check_total_lines()
    logger.debug("wrote default keybindings")

def base_settings(base_path: str):
    """Writes the base settigns for i3 to the same temp file
    """
    # base settings
    logger.warning("writing base settings to tmp file")
    with open(os.path.join(base_path, "i3wm.template"), "r") as f_in,\
            open("./tmp/i3.config", "a") as f_out:

        for line in f_in.readlines():
            f_out.write(line)
    check_total_lines()
    logger.debug("wrote default settings")

def write_colors(config: Dict):
    """Write hex color codes to temp file
    """

    # get the pallet data
    pallet = config['colors']['pallet']

    # read in the entire config file as it stands
    config_text = read_tmp()

    # this is going to be a new copy of the configuration
    config_text_new = []

    # loop through the entire temp file as it stands
    for line in config_text:

        # going through each entrry in the colors
        # color_entry is background, focused, etc.
        found_color = False
        for color_entry in config['i3wm']['colors']:

            # we just found a line in the temp file for some colors
            if f"client.{color_entry}" in line.strip():
                found_color = True
                # start defining a new version of this line. Our goal
                # is to replace the actual words (e.g. background, color6)
                # with the corresponding hex values found in the pallet
                newline = f"client.{color_entry}"

                # the color entry may be a string or list
                if isinstance(config['i3wm']['colors'][color_entry], str):
                    config['i3wm']['colors'][color_entry] = config['i3wm']['colors'][color_entry].split(' ')
                # search through the pallet
                for color_name in config['i3wm']['colors'][color_entry]:

                    # if this runs, a hex code was specified and we don't have to
                    # do anything
                    if '#' in color_name:
                        newline += f"\t{color_name}"

                    # look up the hex code in the pallet
                    else:
                        newline += f"\t{pallet[color_name]}"
                newline += "\n"
                config_text_new.append(newline)
                logger.critical(f"appending to config text new: {newline}")
              # the line we're on isn't related to colors, append as normal
            #else:
        if not found_color:
            config_text_new.append(line)

    # I believe this was for debugging, no need for this anymore
    # check_total_lines()

    # now rewrite the temp file with the colors specified
    write_tmp(config_text_new)

def config_terminal(config: Dict):
    """write information about what terminal to use in the config"""

    # terminal
    terminal = config['i3wm'].get('terminal', 'gnome-terminal')
    config_text = read_tmp()

    if 'bindsym $mod+Return exec' not in config_text:
        config_text.append(f"bindsym $mod+Return exec {terminal}\n")
        write_tmp(config_text)
    else:
        logger.warning("terminal is already established in i3 config, ignoring for now")
    logger.debug("done handling terminal info in i3 config")

def config_font(config: Dict):
    """Write font info to i3 config"""

    font = config['i3wm'].get("font", "pango:JetBrainsMono 10")

    config_text = read_tmp()
    if 'font' not in config_text:
        config_text.append(f"font {font}\n")
        write_tmp(config_text)
    else:
        logger.warning("font is already established in i3 config, ignoring for now")

    logger.debug("wrote font into to i3 config")

def configure_bindsyms(config: Dict):
    """Handle theme-specific bindsyms (there shouldn't be many of these"""

    if 'bindsyms' in config['i3wm']:
        for command in config['i3wm']['bindsyms']:
            match_found = replace_line(
                    "./tmp/i3.config",
                    f"bindsym {command}",
                    f"bindsym {command} {config['i3wm']['bindsyms'][command]}\n")
            if not match_found:
                with open("./tmp/i3.config", "a") as f:
                    f.write(f"bindsym {command} {config['i3wm']['bindsyms'][command]}\n")

    logger.info("finished writing overwritten bindsyms")

def configure_extra_lines(config: Dict):
    """Write any extra lines specified in the config file to i3"""
    # extra lines
    if config['i3wm'].get('extra_lines'):
        with open("./tmp/i3.config", "a") as f:
            for line in config['i3wm']['extra_lines']:
                f.write(f"{line}\n")

def configure_extend(config: Dict, theme_name: str):
    extend_path = os.path.join('.', 'themes', theme_name, 'i3wm.extend')
    if os.path.exists(extend_path):
        config_text = read_tmp()
        with open(extend_path) as f:
            for line in f.readlines():
                config_text.append(line)

        write_tmp(config_text)

