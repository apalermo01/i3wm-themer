import logging

from i3wmthemer.enumeration.attributes import PolybarAttr, XresourcesAttr
from i3wmthemer.models.abstract_theme import AbstractTheme
from i3wmthemer.utils.fileutils import FileUtils
import shutil
import os

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
        polybar_theme = json_file[PolybarAttr.NAME.value]

        if 'use_xresources' in polybar_theme and polybar_theme['x_resources']:
            self.x_resources = json_file[XresourcesAttr.NAME.value]
            self.modules_l = polybar_theme[PolybarAttr.MOD_L.value]
            self.modules_c = polybar_theme[PolybarAttr.MOD_C.value]
            self.modules_r = polybar_theme[PolybarAttr.MOD_R.value]
            self.init_from_xresources()

        else:
            self.background = polybar_theme[PolybarAttr.BACKGROUND.value]
            self.foreground = polybar_theme[PolybarAttr.FOREGROUND.value]
            self.modules_l = polybar_theme[PolybarAttr.MOD_L.value]
            self.modules_c = polybar_theme[PolybarAttr.MOD_C.value]
            self.modules_r = polybar_theme[PolybarAttr.MOD_R.value]
            self.label_un_back = polybar_theme[PolybarAttr.LABEL_UN_BACK.value]
            self.label_un_fore = polybar_theme[PolybarAttr.LABEL_UN_FORE.value]
            self.label_mod_back = polybar_theme[PolybarAttr.LABEL_MOD_BACK.value]
            self.label_mod_fore = polybar_theme[PolybarAttr.LABEL_MOD_FORE.value]
            self.label_foc_back = polybar_theme[PolybarAttr.LABEL_FOC_BACK.value]
            self.label_foc_fore = polybar_theme[PolybarAttr.LABEL_FOC_FORE.value]
            self.label_vis_back = polybar_theme[PolybarAttr.LABEL_VIS_BACK.value]
            self.label_vis_fore = polybar_theme[PolybarAttr.LABEL_VIS_FORE.value]
            self.format_back = polybar_theme[PolybarAttr.FORMAT_BACK.value]
            self.format_fore = polybar_theme[PolybarAttr.FORMAT_FORE.value]
            self.label_open_fore = polybar_theme[PolybarAttr.LABEL_OPEN_FORE.value]
            self.label_close_fore = polybar_theme[PolybarAttr.LABEL_CLOSE_FORE.value]
            self.label_sep_fore = polybar_theme[PolybarAttr.LABEL_SEP_FOREGROUND.value]
            self.format_con_back = polybar_theme[PolybarAttr.FORMAT_CON_BACK.value]
            self.format_con_fore = polybar_theme[PolybarAttr.FORMAT_CON_FORE.value]
            self.format_con_pre_fore = polybar_theme[PolybarAttr.FORMAT_CON_PRE_FORE.value]
            self.ramp_sign_fore = polybar_theme[PolybarAttr.RAMP_SIG_FOREGROUND.value]
            if 'label-active-background' in polybar_theme:
                self.label_active_background = polybar_theme['label-active-background']
            else:
                self.label_active_background = ""
            if 'label-active-underline' in polybar_theme:
                self.label_active_underline = polybar_theme['label-active-underline']
            else:
                self.label_active_underline = ""
    def init_from_xresources(self):
        self.background              = self.x_resources['background']
        self.foreground              = self.x_resources['foreground']
        self.label_un_back           = self.x_resources['color12']
        self.label_un_fore           = self.x_resources['background']
        self.label_mod_back          = self.x_resources['background']
        self.label_mod_fore          = self.x_resources['color0']
        self.label_foc_back          = self.x_resources['color4']
        self.label_foc_fore          = self.x_resources['background']
        self.label_vis_back          = self.x_resources['color12']
        self.label_vis_fore          = self.x_resources['background']
        self.format_back             = self.x_resources['color12']
        self.format_fore             = self.x_resources['background']
        self.label_open_fore         = self.x_resources['color12']
        self.label_close_fore        = self.x_resources['color12']
        self.label_sep_fore          = self.x_resources['color12']
        self.format_con_back         = self.x_resources['color12']
        self.format_con_fore         = self.x_resources['background']
        self.format_con_pre_fore     = self.x_resources['background']
        self.ramp_sign_fore          = self.x_resources['background']
        self.label_active_background = self.x_resources['color0']
        self.label_active_underline  = self.x_resources['color1']

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

        #shutil.copy2(src="
        if FileUtils.locate_file(configuration.polybar_config):
            logger.warning('Located the Polybar configuration file')

            logger.warning('Found the Polybar info in the JSON file')

            FileUtils.replace_line(configuration.polybar_config, 'background =', 'background = ' + self.background)
            FileUtils.replace_line(configuration.polybar_config, 'foreground =', 'foreground = ' + self.foreground)
            FileUtils.replace_line(configuration.polybar_config, 'modules-left', 'modules-left = ' + self.modules_l)
            FileUtils.replace_line(configuration.polybar_config, 'modules-center', 'modules-center = ' + self.modules_c)
            FileUtils.replace_line(configuration.polybar_config, 'modules-right', 'modules-right = ' + self.modules_r)
            FileUtils.replace_line(configuration.polybar_config, 'label-unfocused-background',
                                   'label-unfocused-background = ' + self.label_un_back)
            FileUtils.replace_line(configuration.polybar_config, 'label-unfocused-foreground',
                                   'label-unfocused-foreground = ' + self.label_un_fore)
            FileUtils.replace_line(configuration.polybar_config, 'label-focused-background',
                                   'label-focused-background = ' + self.label_foc_back)
            FileUtils.replace_line(configuration.polybar_config, 'label-focused-foreground',
                                   'label-focused-foreground = ' + self.label_foc_fore)
            FileUtils.replace_line(configuration.polybar_config, 'label-visible-background',
                                   'label-visible-background = ' + self.label_vis_back)
            FileUtils.replace_line(configuration.polybar_config, 'label-visible-foreground',
                                   'label-visible-foreground = ' + self.label_vis_fore)
            FileUtils.replace_line(configuration.polybar_config, 'label-mode-background',
                                   'label-mode-background = ' + self.label_mod_back)
            FileUtils.replace_line(configuration.polybar_config, 'label-mode-foreground',
                                   'label-mode-foreground = ' + self.label_mod_fore)
            FileUtils.replace_line(configuration.polybar_config, 'format-foreground',
                                   'format-foreground = ' + self.format_fore)
            FileUtils.replace_line(configuration.polybar_config, 'format-background',
                                   'format-background = ' + self.format_back)
            FileUtils.replace_line(configuration.polybar_config, 'label-open-foreground',
                                   'label-open-foreground = ' + self.label_open_fore)
            FileUtils.replace_line(configuration.polybar_config, 'label-close-foreground',
                                   'label-close-foreground = ' + self.label_close_fore)
            FileUtils.replace_line(configuration.polybar_config, 'label-separator-foreground',
                                   'label-separator-foreground = ' + self.label_sep_fore)
            FileUtils.replace_line(configuration.polybar_config, 'format-connected-foreground',
                                   'format-connected-foreground = ' + self.format_con_fore)
            FileUtils.replace_line(configuration.polybar_config, 'format-connected-background',
                                   'format-connected-background = ' + self.format_con_back)
            FileUtils.replace_line(configuration.polybar_config, 'format-connected-prefix-foreground',
                                   'format-connected-prefix-foreground = ' + self.format_con_pre_fore)
            FileUtils.replace_line(configuration.polybar_config, 'ramp-signal-foreground',
                                   'ramp-signal-foreground = ' + self.ramp_sign_fore)
            FileUtils.replace_line(configuration.polybar_config, 'label-active-background',
                                    'label-active-background = ' + self.label_active_background)
            FileUtils.replace_line(configuration.polybar_config, 'label-active-underline',
                                    'label-active-underline = ' + self.label_active_underline)
        else:
            logger.error('Failed to locate the Polybar configuration file')

