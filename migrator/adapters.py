from abc import ABC
from sqlite3 import Connection as SQLiteConnection


class Adapter(ABC):

    def setup_database(self):
        raise NotImplementedError

    def is_setup_needed(self) -> bool:
        raise NotImplementedError

    @property
    def current_schema_version(self) -> str:
        raise NotImplementedError

    def execute(self, sql):
        raise NotImplementedError

class SQLiteAdapter:
    def __init__(self, connection: SQLiteConnection):
        self._connection = connection

    def setup_database(self):
        sql = """
            CREATE TABLE 'migrator_metadata' (
                'version' TEXT NOT NULL PRIMARY KEY
            );
            CREATE INDEX 'idx_version' ON 'migrator_metadata' ('version');
        """
        self._connection.executescript(sql)

    def is_setup_needed(self) -> bool:
        sql = """
            SELECT 
                name
            FROM 
                sqlite_master 
            WHERE 
                type ='table' AND 
                name NOT LIKE 'sqlite_%';
        """

        cursor = self._connection.cursor()
        try:
            cursor.execute(sql)
            rows = [x[0] for x in cursor.fetchall()]
            return "migrator_metadata" not in rows
        finally:
            cursor.close()

    @property
    def current_schema_version(self):
        sql = """
            SELECT version FROM migrator_metadata ORDER BY version DESC
        """
        cursor = self._connection.cursor()
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            cursor.close()

    def execute(self, sql_script):
        try:
            self._connection.executescript(sql_script)
            self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            print(e)