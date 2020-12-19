import yaml
import os.path


def get_path():
    for path in [
        "~/.config/nima/config.yaml",
        "~/.config/nima/config.yml",
        "/etc/nima/config.yaml",
        "/etc/nima/config.yml",
    ]:
        path = os.path.expanduser(path)
        if os.path.exists(path):
            return path
    return os.path.expanduser("/etc/nima/config.yaml")


class ConfigFile:
    def __init__(self):
        file = get_path()
        try:
            config = yaml.safe_load(open(file))
            if config is None:
                raise IOError  # to trigger except block
        except IOError:
            # it is ok if we have no config file
            config = {}

        if "projects" not in config:
            config["projects"] = {}
        if "basedomain" not in config:
            config["basedomain"] = "test"
        if "phpfpm" not in config:
            # TODO: check which one
            config["phpfpm"] = "unix:/var/run/php/php7.3-fpm.sock"

        self.config = config
        self.path = file

    def save(self):
        if not os.path.exists(os.path.dirname(self.path)):
            os.mkdir(os.path.dirname(self.path))

        with open(self.path, "w") as file:
            file.write(yaml.dump(self.config))

    def get(self, key):
        return self.config[key]

    def set(self, key, value):
        self.config[key] = value
