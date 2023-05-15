import os
import yaml
import json
from typing import Dict
import shutil
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def backup_file(original_path: str):
    filename = original_path.split('/')[-1].split('.')[0]

    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    dst = os.path.join(*original_path.split('/'), f"{filename}_{timestamp}.backup")

    shutil.copy2(src=original_path, dst=dst)

def initialize(config: Dict, backup: bool, restore: bool):
    """Initializes all config files so everything starts from a clean slate

    :param config: theme configuration
    :param backup: if True, backs up the existing config file - saving a copy in the config's directory
    :param restore: If True, overwrites the config file with the template value
    """
    backup_files = {'vim': backup_vim,
                  'bash': backup_bash,
                  'i3wm': backup_i3}
    for i in init_files:
        init_files[i]()

def backup_vim():

    # if we're backing everything up, 


def init_bash():
    pass


def init_i3():
    pass
