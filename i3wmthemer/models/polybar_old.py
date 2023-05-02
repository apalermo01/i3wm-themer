import logging

from i3wmthemer.enumeration.attributes import PolybarAttr, XresourcesAttr
from i3wmthemer.models.abstract_theme import AbstractTheme
from i3wmthemer.utils.fileutils import FileUtils
import shutil
import os
import configparser

logger = logging.getLogger(__name__)


class PolybarTheme(AbstractTheme):
    """
    Class that contains the Polybar theme attributes.
    """

    def __init__(self, json_file):
        """
        Initializer.
        :param json_file: file that contains the polybar theme.
        """
        self.polybar_theme = json_file[PolybarAttr.NAME.value]
        if 'colors' not in self.polybar_theme:
            self.polybar_theme['colors'] = {}
        self.colors = self.polybar_theme['colors']
        self.xresources = json_file['xresources']
        self.init_colors()

    def init_colors(self):
        """Parse colors for every entry"""
        for color in self.colors:
            self.colors[color] = self.parse_color_line(self.colors[color], self.xresources)

    def init_modules(self, config):
        pass

        # TODO: parse the 'modules' section of the config for custom settings in
        # in polybar config
        if 'modules' not in self.polybar_theme:
            return config
        for m in self.polybar_theme['modules']:
            if m not in config:
                config[m] = self.polybar_theme['modules'][m]
            else:
                config[m].update(self.polybar_theme['modules'][m])
    def load(self, configuration):
        """
        Function that loads the Polybar theme.

        :param configuration: the configuration.
        """

        logger.warning('Applying changes to Polybar configuration file')

        # copy launch script
        src_script = "./scripts/i3wmthemer_bar_launch.sh"
        dest = "/" + os.path.join(*configuration.polybar_config.split('/')[:-1])
        dest_script = os.path.join(dest, "i3wmthemer_bar_launch.sh")
        if not os.path.exists(dest):
            os.makedirs(dest)
        with open(dest_script, "w") as f:
            pass
        shutil.copy2(src_script, dest)

        # now modify the base config file
        if FileUtils.locate_file(configuration.polybar_config):
            logger.warning('Located the Polybar configuration file')

            logger.warning('Found the Polybar info in the JSON file')

            config = configparser.ConfigParser()
            with open(configuration.polybar_config, "r") as f:
                config.read_file(f)

            config['colors'] = self.colors
            config['bar/main']['modules-left'] = self.polybar_theme['modules-left']
            config['bar/main']['modules-center'] = self.polybar_theme['modules-center']
            config['bar/main']['modules-right'] = self.polybar_theme['modules-right']
            config = self.init_modules(config)
            with open(configuration.polybar_config, "w") as f:
                config.write(f)
        else:
            logger.error('Failed to locate the Polybar configuration file')

