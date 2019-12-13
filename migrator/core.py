from .adapters import Adapter
from pathlib import Path
from typing import Union
from datetime import datetime
import logging
import sys
import re


class Migration:
    UP_TOKEN = "-- migrate:up"
    DOWN_TOKEN = "-- migrate:down"

    def __init__(self, version, up="", down="", name=""):
        self._version = version

        self._scripts = {
            self.UP_TOKEN: up,
            self.DOWN_TOKEN: down
        }

        self.name = name

    @property
    def up(self):
        return self._scripts[self.UP_TOKEN]

    @property
    def down(self):
        return self._scripts[self.DOWN_TOKEN]

    @property
    def version(self):
        return datetime.strptime(self._version, "%Y%m%d%H%M%S")

    def load(self, filename: Union[str, Path]):
        if not isinstance(filename, Path):
            filename = Path(filename)

        with open(filename, "r") as f:
            return self.loads(f.read())

    def loads(self, data):
        tokens = [self.UP_TOKEN, self.DOWN_TOKEN]
        map_ = {}
        current_token = None
        for line in data.split("\n"):
            is_token = any([x in line for x in tokens])
            if is_token:
                stripped_line = line.strip()
                map_[stripped_line] = []
                current_token = stripped_line
                continue

            if current_token:
                map_[current_token].append(line)

        for token in tokens:
            if token in map_:
                self._scripts[token] = "".join(map_[token])


class Migrator:
    def __init__(self, adapter: Adapter, migrations_dir: Union[Path, str]):
        self._adapter: Adapter = adapter

        self._migrations_dir: Path = migrations_dir
        if not isinstance(migrations_dir, Path):
            self._migrations_dir = Path(migrations_dir)

        self._logger = logging.getLogger("migrator")
        self._logger.addHandler(logging.StreamHandler(sys.stdout))
        self._logger.setLevel(logging.INFO)
        self._migrations = []

    def add(self, migration: Migration):
        self._migrations.append(migration)

    def add_from_file(self, filename: Union[str, Path]):
        if not isinstance(filename, Path):
            filename = Path(filename)

        if len(filename.stem) < 16:
            raise Exception("Migration file should have a minimum of 16 characters!")
        version = filename.stem[:14]
        if version.isdigit():            
            migration = Migration(version, name=filename.stem)
            migration.load(filename)
            self.add(migration)

    @property
    def migrations(self):
        return sorted(self._migrations, key=lambda x: x.version)

    def migrate(self, version=None):

        min_version = datetime.min
        max_version = datetime.max

        if self._adapter.is_setup_needed():
            self._adapter.setup_database()

        if version:
            max_version = datetime.strptime(version, "%Y%m%d%H%M%S")

        curr_version = self._adapter.current_schema_version
        if (curr_version):
            min_version = datetime.strptime(curr_version, "%Y%m%d%H%M%S")

        def is_valid(v):
            return min_version < v <= max_version

        migrations = [x for x in self.migrations if is_valid(x.version)]

        for migration in migrations:
            self._logger.info("Applying \"%s\"..." % migration.name)
            self._adapter.execute(migration.up)
            self._adapter.execute(
                "INSERT INTO migrator_metadata VALUES ('%s')" % (migration._version)
            )

    def rollback(self, version=None):
        if self._adapter.is_setup_needed():
            raise Exception("No version data available!")

        min_version = datetime.min
        max_version = datetime.strptime(
            self._adapter.current_schema_version,
            "%Y%m%d%H%M%S")
        if version:
            min_version = datetime.strptime(version, "%Y%m%d%H%M%S")

        if min_version > max_version:
            raise Exception("Cannot rollback to a newest version!")

        def is_valid(v):
            return min_version < v <= max_version

        migrations = [x for x in self.migrations if is_valid(x.version)]

        for migration in reversed(migrations):
            self._logger.info("Reverting \"%s\"..." % migration.name)
            self._adapter.execute(migration.down)
            self._adapter.execute(
                "DELETE FROM migrator_metadata WHERE version == '%s'" % (migration._version)
            )
