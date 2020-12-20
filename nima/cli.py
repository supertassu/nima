import click
import os.path
from nima import config, nginx, exceptions


@click.group()
@click.pass_context
def cli(ctx):
    """Utility for managing development nginx config files"""
    ctx.ensure_object(dict)
    ctx.obj["config"] = config.ConfigFile()


@cli.command("config")
@click.pass_context
def cmd_config(ctx):
    """Show the location of the nima configuration file"""
    click.echo(ctx.obj["config"].path)


@cli.command("list")
@click.pass_context
def cmd_list(ctx):
    """List currently installed projects"""
    config: config.ConfigFile = ctx.obj["config"]
    sites = config.get("projects")

    for site_name in sites:
        site: nginx.Site = config.get_site(site_name)
        click.echo(site_name + ": \n  " + "\n  ".join(site.aliases))


@cli.command("add")
@click.pass_context
@click.argument("project_path", type=click.Path(exists=True), default=".")
@click.option(
    "-w",
    "--wildcard",
    is_flag=True,
    help="If specified, also add a wildcard for subdomains of the default domain",
)
def cmd_add(ctx, project_path, wildcard):
    """Create a site for the specified directory"""
    conf: config.ConfigFile = ctx.obj["config"]
    full_path = os.path.realpath(os.path.expanduser(project_path))

    domain_name = os.path.split(full_path)[-1] + "." + conf.get("basedomain")

    site = nginx.Site(full_path, conf)
    site.add_alias(domain_name)
    if wildcard:
        site.add_alias("*." + domain_name)
    site.save()


@cli.command("addalias")
@click.pass_context
@click.argument("domain")
@click.argument("project_path", type=click.Path(exists=True), default=".")
@click.option(
    "-r",
    "--raw",
    is_flag=True,
    help="Do not append the configured base domain to the added alias",
)
def cmd_addalias(ctx, domain, project_path, raw):
    """Add the specified domain as an alias for the specified project path"""
    conf: config.ConfigFile = ctx.obj["config"]
    full_path = os.path.realpath(os.path.expanduser(project_path))
    site: nginx.Site = conf.get_site(full_path)

    if not raw:
        domain += "." + conf.get("basedomain")
    site.add_alias(domain)
    site.save()


@cli.command("deletealias")
@click.pass_context
@click.argument("domain")
@click.argument("project_path", type=click.Path(exists=True), default=".")
@click.option(
    "-r",
    "--raw",
    is_flag=True,
    help="Do not append the configured base domain to the added alias",
)
def cmd_deletealias(ctx, domain, project_path, raw):
    """Delete the specified domain as an alias for the specified project path"""
    conf: config.ConfigFile = ctx.obj["config"]
    full_path = os.path.realpath(os.path.expanduser(project_path))
    site: nginx.Site = conf.get_site(full_path)

    if not raw:
        domain += "." + conf.get("basedomain")
    site.remove_alias(domain)
    site.save()


@cli.command("delete")
@click.pass_context
@click.argument("project_path", type=click.Path(exists=True), default=".")
def cmd_delete(ctx, project_path):
    """Delete site for the specified directory"""
    conf: config.ConfigFile = ctx.obj["config"]
    full_path = os.path.realpath(os.path.expanduser(project_path))
    site: nginx.Site = conf.get_site(full_path)

    site.delete()
