from i3wmthemer.models.abstract_theme import AbstractTheme
from i3wmthemer.models.i3 import I3Theme
from i3wmthemer.models.wallpaper import WallpaperTheme
from i3wmthemer.models.polybar import PolybarTheme
#from i3wmthemer.models.status import StatusbarTheme
from i3wmthemer.models.xresources import XresourcesTheme
from i3wmthemer.models.bashrc import BashTheme
from i3wmthemer.models.vim import VimTheme
import pywal
import os
import yaml

theme_registry = {
        'bash': BashTheme,
        'vimrc': VimTheme,
        }

class Theme(AbstractTheme):
    """
    Class that contains the loaded theme.
    """
    x_resources, i3_theme, polybar_theme, nitrogen_theme = None, None, None, None

    def __init__(self, file):
        """
        Initializer.

        :param file: the JSON file to load from.
        """
        file = self.init_defaults(file)
        file = self.parse_settings(file)
        config_path = file['settings']['config']
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.themes = {
                'xresources': XresourcesTheme(file),
                'i3wm_theme': I3Theme(file),
                'polybar_theme': PolybarTheme(file),
                'wallpaper_theme': WallpaperTheme(file)
        }

        if 'bash' in file:
            self.themes['bash'] = BashTheme(file)

        if 'vimrc' in file:
            self.themes['vimrc'] = VimTheme(file)

    def load(self, configuration, theme_name):
        """
        Batch apply all the themes.

        :param configuration: the configuration.
        """
       # self.x_resources.load(configuration)
       # self.i3_theme.load(configuration)
       # self.polybar_theme.load(configuration)
       # self.wallpaper_theme.load(configuration)
        #self.nitrogen_theme.load(configuration)
        for theme in self.themes:
            self.themes[theme].load(configuration)
            self.extend(theme, configuration, theme_name)
        configuration.refresh_all(self.themes['wallpaper_theme'].wallpaper)

    def extend(self, theme: str, configuration, theme_name: str):
        """If a file ending with the extension .extend lives in the theme folder,
        append the contents of that file to the newly built file.

        :param theme:
        :type theme: str
        :param configuration:
        :param theme_name:
        :type theme_name: str
        """
        theme_module = theme.split('_')[0]
        extend_path = f"./themes/{theme_name}/{theme_module}.extend"
        if theme_module == 'wallpaper':
            return
        config_path = self.config[theme_module]
        if f"{theme_module}.extend" in os.listdir(f"./themes/{theme_name}"):
            with open(extend_path, "r") as f_ext, open(config_path, "a") as f_config:
                extend_content = f_ext.read()
                print('='*80)
                print("appending this content: \n")
                print(extend_content)
                print("to ", config_path)
                print('='*80)
                f_config.write(extend_content)


    def init_defaults(self, file: dict):
        """Initialize default settings that should be present in every theme.
        initializes default settings for general settings, bash, wallpaper, and vim

        :param file:
        :type file: dict
        """
        if 'settings' not in file:
            file['settings'] = {
                    'use_pywal': False,
                    'config': 'config.yaml',
                    'install': './defaults'
                    }

        if 'bash' not in file:
            file['bash'] = {
                    'pywal_colors': True,
                    'git_onefetch': False,
                    'neofetch': True,
                    'extra_lines': []
            }

        if isinstance(file['wallpaper'], str):
            name = file['wallpaper']
            file['wallpaper'] = {
                    'method': 'feh',
                    'name': name
                    }

        if 'vimrc' not in file:
            file['vimrc'] = {
                    'colorscheme': 'gruvbox'
            }

        if 'extra_lines' not in file['vimrc']:
            file['vimrc']['extra_lines'] = ['set bg=dark']
        return file

    def parse_settings(self, file):
        """modify the rest of the config based on what's in the settings section.

        :param file:
        """
        if 'settings' in file and 'use_pywal' in file['settings'] and file['settings']['use_pywal']:
            file = self.populate_file_from_pywal(file)
        return file

    def populate_file_from_pywal(self, file: dict) -> dict:
        """.

        :param file:
        :type file: dict
        :rtype: dict
        """

        wallpaper = file['wallpaper']['name']
        colors = pywal.colors.get("./wallpapers/" + wallpaper)

        ### xresources
        for key in colors['colors']:
            file['xresources'][key] = colors['colors'][key]
        file['xresources']['background'] = colors['special']['background']
        file['xresources']['foreground'] = colors['special']['foreground']
        file['xresources']['cursorcolor'] = colors['special']['cursor']

        color0 = colors['colors']['color0']
        color10 = colors['colors']['color10']
        foreground = colors['special']['foreground']
        color2 = colors['colors']['color2']

        color3 = colors['colors']['color3'] # note - in original themes this color did not show up anywhere else in xresources (e.g. 78824b in 002.json)
        file['xresources']['rofi.color-window'] = f"{color0}, {color10}, {color10}"
        file['xresources']['rofi.color-normal'] = f"{color0}, {foreground}, {color2}, {foreground}, {color3}"
        file['xresources']['rofi.color-active'] = f"{color0}, {foreground}, {color2}, {foreground}, {color3}"
        file['xresources']['rofi.color-urgent'] = f"{color0}, {foreground}, {color2}, {foreground}, {color3}"

        return file
