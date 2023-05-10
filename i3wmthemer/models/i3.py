import logging
from typing import Union, Dict, List


logger = logging.getLogger(__name__)


def check_total_lines():
    with open("./tmp/i3.config", "r") as f:
        total_lines = len([_ for _ in f.readlines()])
    logger.debug(f"{total_lines} lines in ./tmp/i3.config")

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
    """

    # key mappings
    logger.warning("about to write bindsyms to tmp file")
    with open("./defaults/i3_keybindings.template", "r") as f_in,\
        open("./tmp/i3.config", "w") as f_out:

        for line in f_in.readlines():
            f_out.write(line)

    check_total_lines()
    logger.debug("wrote default keybindings")

    # base settings
    logger.warning("writing base settings to tmp file")
    with open(base_path, "r") as f_in,\
            open("./tmp/i3.config", "a") as f_out:

        for line in f_in.readlines():
            f_out.write(line)
    check_total_lines()
    logger.debug("wrote default settings")

    # color data
    pallet = config['colors']['pallet']
    with open("./tmp/i3.config", "r") as f:
        config_text = f.readlines()
    # TODO: handle case where the pallet_key in i3 config doesn't exist in pallet
    # TODO: geneate an image of the color pallet when wal runs, put that in tmp
    # TODO: handle manually specified colors
    config_text_new = []
    for color_entry in config['i3']['colors']:
        for line in config_text:
            if f"client.{color_entry}" in line:
                newline = f"client.{color_entry}"
                for pallet_key in config['i3']['colors'][color_entry]:
                    newline += f"\t{pallet[pallet_key]}"
                config_text_new.append(newline)
            else:
                config_text_new.append(line)
    check_total_lines()
    logger.debug("wrote color data to i3 config")

    # terminal
    terminal =  config['i3'].get('terminal', 'i3-sensible-terminal')

    if 'bindsym $mod+Return exec' not in config_text_new:
        with open('./tmp/i3.config', 'a') as f:
            f.write(f"bindsym $mod+Return exec {terminal}")
    else:
        logger.warning("terminal is already established in i3 config, ignoring for now")
    logger.debug("done handling terminal info in i3 config")

    # font
    font = config['i3'].get("font", "pango:JetBrainsMono 10")
    if 'font' not in config_text_new:
        with open("./tmp/i3.config", "a") as f:
            f.write(f"fond {font}")
    else:
        logger.warning("font is already established in i3 config, ignoring for now")

    logger.debug("wrote font into to i3 config")

    # bindsyms
    # TODO: overwrite bindsyms through config
    if 'bindsyms' in config['i3']:
        with open("./tmp/i3.config", "a") as f:
            for command in config['i3']['bindsyms']:
                f.write(f"bindsym {command} {config['i3']['bindsyms'][command]}")
    logger.debug("finished writing overwritten bindsyms")

    # move config to final location
    with open("./tmp/i3.config", "r") as f_out, open(write_path, "w") as f_in:
        for r in f_out.readlines():
            f_in.write(r)
    return config
