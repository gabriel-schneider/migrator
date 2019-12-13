import pytest
import sqlite3
from pathlib import Path
from datetime import datetime
from migrator import Migrator, SQLiteAdapter, Migration


def table_exists(conn, table_name):
        sql = """
            SELECT 
                name
            FROM 
                sqlite_master 
            WHERE 
                type ='table' AND 
                name NOT LIKE 'sqlite_%';
        """

        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = [x[0] for x in cursor.fetchall()]
            return table_name in rows
        finally:
            cursor.close()


def test_migration():
    connection = sqlite3.connect(":memory:")
    adapter = SQLiteAdapter(connection)
    migrator = Migrator(adapter, "")

    migrations = [
        """
        -- migrate:up
        CREATE TABLE 'users' (
            'email' TEXT
        );

        -- migrate:down
        DROP TABLE 'users'""",
        """
        -- migrate:up
        ALTER TABLE 'users'
            ADD 'name' TEXT

        -- migrate:down
        ALTER TABLE 'users'
            DROP COLUMN 'name'
        """
    ]

    for migration in migrations:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        mig = Migration(version=now)
        mig.loads(migration)
        migrator.add(mig)

    migrator.migrate()

    assert table_exists(connection, "users")


def test_migration_from_file():
    connection = sqlite3.connect(":memory:") 
    adapter = SQLiteAdapter(connection)
    migrator = Migrator(adapter, "")

    for path in Path("tests/data/migrations").iterdir():
        migrator.add_from_file(path)

    migrator.migrate()

    assert table_exists(connection, "user")
    assert table_exists(connection, "artist")
    assert table_exists(connection, "permission")
    assert table_exists(connection, "media")
    assert table_exists(connection, "users_permissions")


def test_rollback_without_version():
    connection = sqlite3.connect(":memory:") 
    adapter = SQLiteAdapter(connection)
    migrator = Migrator(adapter, "")

    for path in Path("tests/data/migrations").iterdir():
        migrator.add_from_file(path)

    migrator.migrate()
    migrator.rollback()

    assert not table_exists(connection, "user")
    assert not table_exists(connection, "artist")
    assert not table_exists(connection, "permission")
    assert not table_exists(connection, "media")
    assert not table_exists(connection, "users_permissions")


def test_load_migrations_from_directory():
    connection = sqlite3.connect(":memory:")
    adapter = SQLiteAdapter(connection)
    migrator = Migrator(adapter, "")

    migrator.add_from_directory("tests/data/migrations")

    def has_migration(name):
        for migration in migrator.migrations:
            if migration.name == name:
                return True
        return False

    assert has_migration("20191127162300_user_table")
    assert has_migration("20191127170816_users_permissions_table")
    assert has_migration("20191207231210_add_media_mime")
