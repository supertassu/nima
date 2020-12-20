import yaml
import os.path
from nima.nginx import Site, from_config


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


class Option:
    def __init__(self, name, default=None):
        self.name = name
        self.default = default


class ConfigFile:
    def __init__(self):
        file = get_path()
        try:
            config = yaml.safe_load(open(file))
            if config is None:
                raise IOError  # to trigger except block
        except IOError:  # it is ok if we have no config file
            # it is ok if we have no config file
            config = {}

        if "projects" not in config:
            config["projects"] = {}
        if "basedomain" not in config:
            config["basedomain"] = "test"
        if "nginx_sites_base_path" not in config:
            config["nginx_sites_base_path"] = "/etc/nginx/sites-enabled"
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

    def get_site(self, full_path) -> Site:
        return from_config(full_path, self)
