"""Save the content of the database in an SQL file (data/backup_db.sql).

Usage (from the root of the repository):
    uv run --project backend python backend/src/export_db.py
"""

import os
from datetime import datetime
from pathlib import Path

import dotenv

from dao.db_connection import DBConnection


class ExportDatabase:
    def __init__(self):
        self.base_path = Path(__file__).resolve().parent.parent.parent
        self.output_path = self.base_path / "data" / "backup_db.sql"

    def run(self):
        dotenv.load_dotenv()

        schema = os.environ["POSTGRES_SCHEMA"]

        tables = [
            "users",
            "stations",
            "stationrecords",
            "favorites",
        ]

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                with open(self.output_path, "w", encoding="utf-8") as file:
                    for table in tables:
                        cursor.execute(f"SELECT * FROM {schema}.{table}")

                        rows = cursor.fetchall()

                        if not rows:
                            continue

                        columns = list(rows[0].keys())

                        file.write(f"\n-- Data for {table}\n")

                        for row in rows:
                            values = []

                            for column in columns:
                                value = row[column]

                                if value is None:
                                    values.append("NULL")
                                elif isinstance(value, (str, datetime)):
                                    value = str(value).replace("'", "''")
                                    values.append(f"'{value}'")
                                else:
                                    values.append(str(value))

                            file.write(
                                f"INSERT INTO {schema}.{table} "
                                f"({', '.join(columns)}) "
                                f"VALUES ({', '.join(values)});\n"
                            )

                    file.write(
                        f"\nSELECT setval(pg_get_serial_sequence('{schema}.users', 'id_user'), "
                        f"(SELECT MAX(id_user) FROM {schema}.users));\n"
                    )

        print(f"Database exported to {self.output_path}")


if __name__ == "__main__":
    ExportDatabase().run()
