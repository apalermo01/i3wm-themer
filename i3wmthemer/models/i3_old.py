import logging

from i3wmthemer.enumeration.attributes import I3Attr, XresourcesAttr
from i3wmthemer.models.abstract_theme import AbstractTheme
from i3wmthemer.utils.fileutils import FileUtils
from textwrap import dedent
logger = logging.getLogger(__name__)


class I3Theme(AbstractTheme):
    """
    Class that contains the attributes of the i3 theme that should be loaded.
    """
    def __init__(self, json_file):
        """
        Initializer.

        :param json_file: JSON file that contains the theme data.
        """
        self.i3theme = json_file['i3']

        self.x_resources = json_file['xresources']
        self.init_colors()

        ### default terminal
        if 'terminal' not in self.i3theme:
            self.i3theme['terminal'] = 'gnome-terminal'



    def load(self, configuration):
        """Load settings into i3 config file.

        :param configuration:
        """
        # load colors
        self.write_colors(configuration)

        if "font" in self.i3theme:
            self.init_font(configuration)
        self.set_terminal(configuration)
        self.init_bindsyms(configuration)


    def init_bindsyms(self, configuration):
        """Add theme-specific bindsyms to i3 config.

        :param configuration:
        """

        if 'bindsyms' not in self.i3theme:
            return

        for command in self.i3theme['bindsyms']:
            match_found = FileUtils.replace_line(configuration.i3_config,
                                         f"bindsym {command}",
                                         f"bindsym {command} {self.i3theme['bindsyms'][command]}")
            if not match_found:
                cmd = f"bindsym {command} {self.i3theme['bindsyms'][command]}"
                FileUtils.append_line(configuration.i3, cmd)

    def init_font(self, configuration):
        """Add font info to i3 config.

        :param configuration:
        """
        text = f"font {self.i3theme['font']}\n"
        FileUtils.append_line(configuration.i3, text)

    def set_terminal(self, configuration):
        """Set the terminal to run with $mod+Return.

        :param configuration:
        """
        text = f"bindsym $mod+Return exec {self.i3theme['terminal']}\n"
        FileUtils.append_line(configuration.i3, text)

    def init_colors(self):
        """Copy the color entries from the xresources part of the config to the colors for i3"""

        focused_list = ['foreground', 'background', 'foreground', 'color12', 'color12']
        unfocused_list = ['foreground', 'background', 'foreground', 'color4', 'color4']
        focused_inactive_list = ['foreground', 'background', 'foreground', 'color4', 'color4']
        urgent_list =  ['foreground', 'background', 'foreground', 'color4', 'color4']
        placeholder_list =  ['foreground', 'background', 'foreground', 'color4', 'color4']

        if "colors" not in self.i3theme:
            self.background = self.x_resources[XresourcesAttr.BACKGROUND.value]
            self.focused = " ".join([self.x_resources[i] for i in focused_list])
            self.unfocused = " ".join([self.x_resources[i] for i in unfocused_list])
            self.inactive = " ".join([self.x_resources[i] for i in focused_inactive_list])
            self.urgent = " ".join([self.x_resources[i] for i in urgent_list])
            self.placeholder = " ".join([self.x_resources[i] for i in placeholder_list])
        else:
            if 'background' in self.i3theme['colors']:
                self.background = self.parse_color_line(self.i3theme['colors']['background'], self.x_resources)
            else:
                self.background = self.x_resources[XresourcesAttr.BACKGROUND.value]

            if 'focused' in self.i3theme['colors']:
                self.focused = self.parse_color_line(self.i3theme['colors']['focused'], self.x_resources)
            else:
                self.focused = " ".join([self.x_resources[i] for i in focused_list])

            if 'unfocused' in self.i3theme['colors']:
                self.unfocused = self.parse_color_line(
                                    self.i3theme['colors']['unfocused'],
                                    self.x_resources)
            else:
                self.unfocused = " ".join([self.x_resources[i] for i in unfocused_list])

            if 'focused_inactive' in self.i3theme['colors']:
                self.inactive = self.parse_color_line(
                                    self.i3theme['colors']['focused_inactive'],
                                    self.x_resources)
            else:
                self.inactive = " ".join([self.x_resources[i] for i in focused_inactive_list])

            if 'urgent' in self.i3theme['colors']:
                self.urgent = self.parse_color_line(self.i3theme['colors']['urgent'], self.x_resources)
            else:
                self.urgent = " ".join([self.x_resources[i] for i in urgent_list])

            if 'placeholder' in self.i3theme['colors']:
                self.placeholder = self.parse_color_line(self.i3theme['colors']['placeholder'], self.x_resources)
            else:
                self.placeholder = " ".join([self.x_resources[i] for i in placeholder_list])

    def write_colors(self, configuration):
        color_entry = dedent(f"""
        client.background {self.background} \n
        client.focused {self.focused} \n
        client.unfocused {self.unfocused} \n
        client.focused_inactive {self.inactive} \n
        client.urgent {self.urgent} \n
        client.placeholder {self.placeholder} \n
        """)

        FileUtils.append_line(configuration.i3, color_entry)

