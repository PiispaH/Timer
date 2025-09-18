import os
import sqlite3
from datetime import datetime
from typing import Dict
from utils import DB_PATH


class DatabaseHandler:
    def __init__(self):
        self.db = None
        self._open_db()

    def new_category(self, category: str) -> int:
        """Adds a new category to the DB and returns the id for it"""
        cursor = self.db.execute(
            """
            INSERT INTO Categories (name)
                VALUES (?)
            """,
            [category],
        )
        self.db.execute("COMMIT")
        return cursor.lastrowid

    def add_record(self, category_id: int, start: datetime, end: datetime):
        """Adds a record to the database."""
        cursor = self.db.execute(
            """
            INSERT INTO Records (category_id, start, end)
                VALUES (?, ?, ?)
            """,
            [category_id, start, end],
        )
        self.db.execute("COMMIT")
        return cursor.lastrowid

    def get_categories(self) -> Dict[str, int]:
        """Fetches the categories from the database. Returns a mapping from name to id."""
        categories = self.db.execute(
            """
            SELECT name, id
            FROM Categories
            """
        ).fetchall()
        return {data[0]: data[1] for data in categories}

    def _open_db(self):
        """Opens a connection to the database. If the first time,
        also creates the tables."""
        if not os.path.exists(DB_PATH):
            os.mkdir(os.path.dirname(DB_PATH))
            self.db = sqlite3.connect(DB_PATH)
            self._create_tables()
        else:
            self.db = sqlite3.connect(DB_PATH)

    def _create_tables(self):
        self.db.execute(
            """
            CREATE TABLE Categories (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
            """
        )
        self.db.execute(
            """
            CREATE TABLE Records (
                id INTEGER PRIMARY KEY,
                category_id INTEGER,
                start DATETIME,
                end DATETIME,
                FOREIGN KEY (category_id) REFERENCES Categories(id)
            )
            """
        )

    def close(self):
        self.db.close()
        if False:  # Debugging
            if os.path.exists(DB_PATH):
                os.remove(DB_PATH)
