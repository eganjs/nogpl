import click
import toml


@click.group()
def cli():
    pass


@cli.group()
def report():
    pass


@report.command()
@click.option("-f", "--lock-file", type=click.File("r"), default="poetry.lock")
def all(lock_file):
    dependencies_metadata = toml.load(lock_file)
    if "package" in dependencies_metadata:
        for package in dependencies_metadata["package"]:
            click.echo(package["name"] + " " + package["version"] + " BSD-3-Clause")
