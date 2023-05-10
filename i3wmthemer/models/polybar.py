import configparser
import os
import shutil

def parse_polybar(config, write_path):

    settings = config['polybar']
    polybar_config = configparser.ConfigParser()
    polybar_config.read("./defaults/polybar.template")

    # TODO: load polybar config from theme folder
    # TODO: modules-left, modules-right, and modules-center
    # TODO: lay out exactly how default settings and theme specific settings should interact
    # TODO: rename colors in template polybar config
    # TODO: handle overwrites
    polybar_config['colors'] = config['colors']['pallet']


    with open("./tmp/polybar.ini", "w") as f:
        polybar_config.write(f)

    # save to final file
    with open("./tmp/polybar.ini", "r") as f_out, open(write_path, "w") as f_in:
        for line in f_out.readlines():
            f_in.write(line)

    # launch script
    src_script = "./scripts/i3wmthemer_bar_launch.sh"
    dest = "/" + os.path.join(*write_path.split('/')[:-1])
    dest_script = os.path.join(dest, "i3wmthemer_bar_launch.sh")
    if not os.path.exists(dest):
        os.makedirs(dest)
    with open(dest_script, 'w') as f:
        pass
    shutil.copy2(src_script, dest)
