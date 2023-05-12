import os
import logging
from typing import Dict
import shutil

logger = logging.getLogger(__name__)

def parse_picom(config: Dict,
                write_path: str,
                theme_name: str):
    theme_path = os.path.join(".", "themes", theme_name, "picom.conf")
    if os.path.exists(theme_path):
        logger.info("found picom.conf")
        shutil.copy(src=theme_path, dst=write_path)

