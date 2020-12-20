# nima

```
$ sudo nima
Usage: nima [OPTIONS] COMMAND [ARGS]...

  Utility for managing development nginx config files

Options:
  --help  Show this message and exit.

Commands:
  add          Create a site for the specified directory
  addalias     Add the specified domain as an alias for the specified project path
  config       Show the location of the nima configuration file
  delete       Delete site for the specified directory
  deletealias  Delete the specified domain as an alias for the specified project path
  list         List currently installed projects
```

## Installing

I haven't published Nima into pypi yet since it still has a couple issues I would like to do before publishing.
If you would still like to install nima, you can install it from Git:

```
$ sudo python -m pip install git+https://github.com/supertassu/nima.git
```

Note that there might be some issues (especially when not running Debian stable (currently buster)).

## Usage

TODO. See help above. You might want to run nima as root as it wants to restart services and write
to `/etc/nginx/sites-enabled`.

## License

MIT.
