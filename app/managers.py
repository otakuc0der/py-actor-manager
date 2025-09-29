import sqlite3
import re
from app.models import Actor


class ActorManager:
    def __init__(
            self,
            db_name: str,
            table_name: str
    ) -> None:
        if not re.match(
                r"^[A-Za-z_][A-Za-z0-9_]*$",
                table_name
        ):
            raise ValueError(
                f"Invalid table name: {table_name}"
            )
        self.db_name = db_name
        self.table_name = table_name
        self._connection = sqlite3.connect(self.db_name)

    def create(
            self,
            first_name: str,
            last_name: str
    ) -> int | None:
        cursor = self._connection.execute(
            f"INSERT INTO {self.table_name} "
            "(first_name, last_name) VALUES (?, ?)",
            (first_name, last_name)
        )
        self._connection.commit()
        return cursor.lastrowid

    def all(self) -> list[Actor]:
        cursor = self._connection.execute(
            f"SELECT id, first_name, last_name "
            f"FROM {self.table_name}"
        )
        return [
            Actor(*entity_tuple)
            for entity_tuple in cursor.fetchall()
        ]

    def update(
            self,
            pk: int,
            new_first_name: str,
            new_last_name: str
    ) -> int | None:
        cursor = self._connection.execute(
            f"UPDATE {self.table_name} "
            "SET first_name = ?, last_name = ? "
            "WHERE id = ?",
            (new_first_name, new_last_name, pk)
        )
        self._connection.commit()
        return cursor.lastrowid

    def delete(self, pk: int) -> int | None:
        cursor = self._connection.execute(
            f"DELETE FROM {self.table_name} "
            "WHERE id = ?",
            (pk,)
        )
        self._connection.commit()
        return cursor.lastrowid

    def close(self) -> None:
        self._connection.close()
