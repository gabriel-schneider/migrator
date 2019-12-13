import os
import click
from datetime import datetime


MIGRATOR = None
MIGRATIONS_DIR = None


@click.group()
@click.option(
    "--migrations-dir",
    default="migrations",
    help="Migrations directory")
def cli(migrations_dir):
    if not os.path.exists(migrations_dir):
        os.makedirs(migrations_dir)

    global MIGRATIONS_DIR
    MIGRATIONS_DIR = migrations_dir


@cli.command()
@click.argument("name")
def new(name):
    version = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.join(MIGRATIONS_DIR, "%s_%s.sql" % (version, name))
    with open(filename, "w") as file:
        file.write("-- migrate:up\n\n\n-- migrate:down\n\n\n")
