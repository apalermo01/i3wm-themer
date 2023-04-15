import logging
from typing import Union, Dict, List


logger = logging.getLogger(__name__)


def parse_i3theme(base_path: str = "./defaults/i3wm.template",
                  append_list: Union[List, None] = None,
                  configuration_data: Union[Dict, None] = None):
    """
    Configures i3wm settings from a base file

    v1:
    First reads in the file located at base path
    then appends any extra configuration settings from the data found in append_list
    then adds the configuration info found in the configuration_data dictionary
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
    with open("./defaults/i3_keybindings.template", "r") as f_in,\
        open("./tmp/i3.config", "w") as f_out:

        for line in f_in.readlines():
            f_out.write(line)

    # base settings
    with open(base_path, "r") as f_in,\
            open("./tmp/i3.config", "a") as f_out:

        for line in f_in.readlines():
            f_out.write(line)

    # color data
    pallet = configuration_data['colors']['pallet']
    with open("./tmp/i3.config", "r") as f:
        config_text = f.readlines()

    # TODO: handle case where the pallet_key in i3 config doesn't exist in pallet
    # TODO: geneate an image of the color pallet when wal runs, put that in tmp
    config_text_new = []
    for color_entry in configuration_data['i3']['colors']:
        for line in config_text:
            if f"client.{color_entry}" in line:
                newline = f"client.{color_entry}"
                for pallet_key in configuration_data['i3']['colors'][color_entry]:
                    newline += f"\t{pallet[pallet_key]}"
                config_text_new.append(newline)
            else:
                config_text_new.append(line)
    with open("./tmp/i3.config", "w") as f:
        f.writelines(config_text_new)

    # terminal
    terminal =  configuration_data['i3'].get('terminal', 'i3-sensible-terminal')

    if 'bindsym $mod+Return exec' not in config_text_new:
        with open('./tmp/i3.config', 'a') as f:
            f.write(f"bindsym $mod+Return exec {terminal}")
    else:
        print("WARNING: terminal is already established in i3 config, ignoring for now")

    # font
    font = configuration_data['i3'].get("font", "pango:JetBrainsMono 10")
    if 'font' not in config_text_new:
        with open("./tmp/i3.config", "a") as f:
            f.write(f"fond {font}")
    else:
        print("WARNING: font is already established in i3 config, ignoring for now")

def add_configuration_data(configuration_data: Dict):
    """
    This function parses the json dict
    """
    pass



