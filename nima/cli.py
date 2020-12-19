import click
import os.path
from nima import config, nginx


@click.group()
@click.pass_context
def cli(ctx):
    """Utility for managing development nginx config files"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config.ConfigFile()


@cli.command('config')
@click.pass_context
def cmd_config(ctx):
    """Show the location of the nima configuration file"""
    click.echo(ctx.obj['config'].path)


@cli.command('list')
@click.pass_context
def cmd_list(ctx):
    """List currently installed projects"""
    for project in ctx.obj['config'].get('projects'):
        data = ctx.obj['config'].get('projects')[project]
        click.echo(project + ": " + ', '.join(data['hosts']))


@cli.command()
@click.pass_context
@click.argument('path', type=click.Path())
def add(ctx, path):
    """Link the specified directory"""
    conf: config.ConfigFile = ctx.obj['config']
    full_path = os.path.realpath(os.path.expanduser(path))
    if not os.path.isdir(full_path):
        raise click.ClickException("Path does not exist")

    domain_name = os.path.split(full_path)[-1] + '.' + conf.get('basedomain')

    site = nginx.Site(full_path)
    site.add_alias(domain_name)
    site.save()

    project_config = conf.get('projects')
    project_config[full_path] = site.to_dict()
    conf.set('projects', project_config)
    conf.save()

