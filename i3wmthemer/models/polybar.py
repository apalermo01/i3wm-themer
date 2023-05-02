import configparser

def parse_polybar(config):

    settings = config['polybar']
    polybar_config = configparser.ConfigParser()
    polybar_config.read("./defaults/polybar.template")
    print(polybar_config.sections())
    print(polybar_config['colors'])

    # TODO: load polybar config from theme folder
    # TODO: lay out exactly how default settings and theme specific settings should interact
    # TODO: rename colors in template polybar config
    polybar_config['colors'] = config['colors']['pallet']


    with open("./tmp/polybar.ini", "w") as f:
        polybar_config.write(f)
