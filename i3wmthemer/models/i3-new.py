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

    # read file at base path

def add_configuration_data(configuration_data: Dict):
    """
    This function parses the json dict
    """
    pass



