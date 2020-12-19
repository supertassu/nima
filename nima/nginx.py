import os
import os.path
from subprocess import call
from jinja2 import Template
from nima.exceptions import NimaException

config_base_path = "/etc/nginx/sites-enabled"


def restart_nginx():
    call(['systemctl', 'restart', 'nginx'])


class Site:
    def __init__(self, directory: str):
        self.directory = directory
        self.webroot = None
        self.file = None
        self.aliases = []

    def locate_webroot(self) -> str:
        for check, webroot in [
            ('public/index.php', 'public'),
            ('public/index.html', 'public'),
            ('public_html/index.php', 'public_html'),
            ('public_html/index.html', 'public_html'),
            ('webroot/index.php', 'webroot'),
            ('webroot/index.html', 'webroot'),
        ]:
            if os.path.exists(os.path.join(self.directory, check)):
                return os.path.join(self.directory, webroot)
        return self.directory

    def get_webroot(self) -> str:
        if self.webroot is None:
            self.webroot = self.locate_webroot()
        return self.webroot

    def get_file(self) -> str:
        if self.file is None:
            if len(self.aliases) == 0:
                raise
            self.file = os.path.join(config_base_path, self.aliases[0] + '.conf')
        return self.file

    def add_alias(self, alias: str):
        if alias in self.aliases:
            return
        self.aliases.append(alias)

    def remove_alias(self, alias: str):
        self.aliases.remove(alias)

    def save(self):
        webroot = self.get_webroot()
        file = self.get_file()

        template_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'site.conf')
        with open(template_file, 'r', encoding='utf-8') as f:
            template = Template(f.read())
        content = template.render(
            names=' '.join(self.aliases),
            root=webroot,
            phpfpm='unix:/var/run/php/php7.3-fpm.sock',  # TODO: from config
        )

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        restart_nginx()

    def delete(self):
        file = self.get_file()
        with open(file, 'r', encoding='utf-8') as f:
            first = f.readline()
            if first != "# Managed by Nima\n":
                raise NimaException("File doesn't seem to be managed by this script")

        os.remove(file)
        restart_nginx()

    def to_dict(self) -> dict:
        return {
            "webroot": self.get_webroot(),
            "file": self.get_file(),
            "aliases": self.aliases,
        }


def from_dict(directory: str, data: dict) -> Site:
    site = Site(directory)
    if 'aliases' in data:
        for alias in data['aliases']:
            site.add_alias(alias)
    if 'file' in data:
        site.file = data['file']
    if 'webroot' in data:
        site.webroot = data['webroot']
    return site

