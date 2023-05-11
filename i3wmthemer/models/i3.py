import logging
from typing import Union, Dict, List
from i3wmthemer.fileutils import replace_line

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
        f.writelines(f)

def parse_i3theme(config: Dict,
                  write_path: str,
                  base_path: str = "./defaults/i3wm.template",
                  append_list: Union[List, None] = None,):
    """
    Configures i3wm settings from a base file

    v1:
    First reads in the file located at base path
    then appends any extra configuration settings from the data found in append_list
    then adds the configuration info found in the config dictionary
    possible keys for configuration_dat dictionary:
        bindsyms: list of custom keybindings specific to the theme
            TODO: what if we optionally put this info somewhere easily accessible?
        default_terminal: name of the default terminal to use (bindsym)

    v2:
    - read in base components from defaults: bindsyms and templates
    - append additional lines from theme template
    - read color info from appropriate color files (need to design colors module first)
    - update config with color information based on palett and config file
    - overwrite lines based on json file

    v3: start with a list of lines to put in the file, at some point write them to a tmp file
    """
    # initialize tmep file
    with open("tmp/i3.config", "w") as f:
        logger.warning("overwrote i3.config temp file")

    key_mappings()
    base_settings(base_path=base_path)
    write_colors(config=config)
    config_terminal(config=config)
    configure_bindsyms(config=config)
    configure_extra_lines(config=config)

    # move config to final location
    with open("./tmp/i3.config", "r") as f_out, open(write_path, "w") as f_in:
        for r in f_out.readlines():
            f_in.write(r)
    return config

def key_mappings():
    """Writes the default keybindings to a temp file
    """
    logger.warning("about to write bindsyms to tmp file")
    with open("./defaults/i3_keybindings.template", "r") as f:
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
    with open(base_path, "r") as f_in,\
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
    with open("./tmp/i3.config", "r") as f:
        config_text = f.readlines()

    # this is going to be a new copy of the configuration
    config_text_new = []

    # loop through the entire temp file as it stands
    for line in config_text:

        # going through each entrry in the colors
        # color_entry is background, focused, etc.
        found_color = False
        for color_entry in config['i3']['colors']:
            logger.info(f"modifying i3 colors for {color_entry}")


              # we just found a line in the temp file for some colors
            if f"client.{color_entry}" in line.strip():
                found_color = True
                # start defining a new version of this line. Our goal
                # is to replace the actual words (e.g. background, color6)
                # with the corresponding hex values found in the pallet
                newline = f"client.{color_entry}"

                  # search through the pallet
                for color_name in config['i3']['colors'][color_entry]:

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
    with open("./tmp/i3.config", "w") as f:
        f.writelines(config_text_new)

def config_terminal(config: Dict):
    """write information about what terminal to use in the config"""

    # terminal
    terminal = config['i3'].get('terminal', 'i3-sensible-terminal')

    with open("./tmp/i3.config", "r") as f:
        config_text = f.readlines()

    if 'bindsym $mod+Return exec' not in config_text:
        with open('./tmp/i3.config', 'a') as f:
            f.write(f"bindsym $mod+Return exec {terminal}\n")
    else:
        logger.warning("terminal is already established in i3 config, ignoring for now")
    logger.debug("done handling terminal info in i3 config")

def config_font(config: Dict):
    """Write font info to i3 config"""

    font = config['i3'].get("font", "pango:JetBrainsMono 10")

    config_text = read_tmp()
    if 'font' not in config_text:
        config_text.append(f"font {font}\n")
        write_tmp(config_text)
    else:
        logger.warning("font is already established in i3 config, ignoring for now")

    logger.debug("wrote font into to i3 config")

def configure_bindsyms(config: Dict):
    """Handle theme-specific bindsyms (there shouldn't be many of these"""

    if 'bindsyms' in config['i3']:
        for command in config['i3']['bindsyms']:
            match_found = replace_line(
                    "./tmp/i3.config",
                    f"bindsym {command}",
                    f"bindsym {command} {config['i3']['bindsyms'][command]}\n")
            if not match_found:
                with open("./tmp/i3.config", "a") as f:
                    f.write(f"bindsym {command} {config['i3']['bindsyms'][command]}\n")

    logger.info("finished writing overwritten bindsyms")

def configure_extra_lines(config: Dict):
    """Write any extra lines specified in the config file to i3"""
    # extra lines
    if config['i3'].get('extra_lines'):
        with open("./tmp/i3.config", "a") as f:
            for line in config['i3']['extra_lines']:
                f.write(f"{line}\n")

