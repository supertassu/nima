import click
import os.path
from nima import config, nginx, exceptions


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
        site: nginx.Site = nginx.from_dict(project, ctx.obj['config'].get('projects')[project])
        click.echo(project + ": \n  " + "\n  ".join(site.aliases))


@cli.command('add')
@click.pass_context
@click.argument('project_path', type=click.Path(exists=True), default='.')
@click.option('-w', '--wildcard', is_flag=True, help='If specified, also add a wildcard for subdomains of the default '
                                                     'domain')
def cmd_add(ctx, project_path, wildcard):
    """Create a site for the specified directory"""
    conf: config.ConfigFile = ctx.obj['config']
    full_path = os.path.realpath(os.path.expanduser(project_path))

    domain_name = os.path.split(full_path)[-1] + '.' + conf.get('basedomain')

    site = nginx.Site(full_path)
    site.add_alias(domain_name)
    if wildcard:
        site.add_alias('*.' + domain_name)
    site.save()

    project_config = conf.get('projects')
    project_config[full_path] = site.to_dict()
    conf.set('projects', project_config)
    conf.save()


@cli.command('addalias')
@click.pass_context
@click.argument('domain')
@click.argument('project_path', type=click.Path(exists=True), default='.')
@click.option('-r', '--raw', is_flag=True, help='Do not append the configured base domain to the added alias')
def cmd_addalias(ctx, domain, project_path, raw):
    """Add the specified domain as an alias for the specified project path"""
    conf: config.ConfigFile = ctx.obj['config']
    project_config = conf.get('projects')
    full_path = os.path.realpath(os.path.expanduser(project_path))

    if full_path not in project_config:
        raise exceptions.NotAProjectDirectory(full_path)
    site: nginx.Site = nginx.from_dict(full_path, project_config[full_path])

    if not raw:
        domain += '.' + conf.get('basedomain')
    site.add_alias(domain)

    project_config[full_path] = site.to_dict()
    conf.set('projects', project_config)
    conf.save()


@cli.command('deletealias')
@click.pass_context
@click.argument('domain')
@click.argument('project_path', type=click.Path(exists=True), default='.')
@click.option('-r', '--raw', is_flag=True, help='Do not append the configured base domain to the added alias')
def cmd_deletealias(ctx, domain, project_path, raw):
    """Delete the specified domain as an alias for the specified project path"""
    conf: config.ConfigFile = ctx.obj['config']
    project_config = conf.get('projects')
    full_path = os.path.realpath(os.path.expanduser(project_path))

    if full_path not in project_config:
        raise exceptions.NotAProjectDirectory(full_path)
    site: nginx.Site = nginx.from_dict(full_path, project_config[full_path])

    if not raw:
        domain += '.' + conf.get('basedomain')
    site.remove_alias(domain)

    project_config[full_path] = site.to_dict()
    conf.set('projects', project_config)
    conf.save()


@cli.command('delete')
@click.pass_context
@click.argument('project_path', type=click.Path(exists=True), default='.')
def cmd_delete(ctx, project_path):
    """Delete site for the specified directory"""
    conf: config.ConfigFile = ctx.obj['config']
    project_config = conf.get('projects')
    full_path = os.path.realpath(os.path.expanduser(project_path))

    if full_path not in project_config:
        raise exceptions.NotAProjectDirectory(full_path)

    site: nginx.Site = nginx.from_dict(full_path, project_config[full_path])
    site.delete()

    del project_config[full_path]
    conf.set('projects', project_config)
    conf.save()

