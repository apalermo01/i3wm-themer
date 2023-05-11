import logging
import os
import shutil
from typing import Dict
from textwrap import dedent


logger = logging.getLogger(__name__)


def parse_bash(config: Dict,
               write_path: str):

    # TODO: don't hardcode paths
    bash_config = config['bash']

    if 'extra_lines' not in bash_config:
        bash_config['extra_lines'] = []

    if bash_config.get('pywal_colors'):
        wp_name = config['wallpaper']
        wallpaper_path = os.path.expanduser(f"~/Pictures/wallpapers/{wp_name}")
        bash_config['extra_lines'].append(dedent(f"""
        wal -n -e -i {wallpaper_path} > /dev/null \n
        """))

    if bash_config.get('git_onefetch'):
        bash_config['extra_lines'].append(dedent("""
                function show_onefetch() {
                    if [ -d .git ]; then
                        onefetch
                    fi
                }
                function cd() { builtin cd "$@" && show_onefetch; }
                \n
            """))

    if bash_config.get('onefetch'):
        bash_config['extra_lines'].append("neofetch'\n")

    bashrc_path = os.path.expanduser("~/.bashrc")
    bash_template_path = "./defaults/bash.template"

    # write to file
    with open(bashrc_path, 'w') as f_out, open(bash_template_path, "r") as f_template:
        for line in f_template.readlines():
            f_out.write(line)

        for line in bash_config['extra_lines']:
            f_out.write(line)
