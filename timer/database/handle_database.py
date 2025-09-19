import os
import sqlite3
from datetime import datetime
from typing import Dict
from utils import DATA_FOLDER_PATH
from ..category import Category, CategoryManager


class DatabaseHandler:
    def __init__(self, db_name="database"):
        self.db = None
        self._filepath = os.path.join(DATA_FOLDER_PATH, db_name + ".db")
        self._open_db()

    def new_category(self, category: Category) -> int:
        """Adds a new category to the DB and returns the id for it"""
        cursor = self.db.execute(
            """
            INSERT INTO Categories (id, name)
                VALUES (?, ?)
            """,
            [category.id, category.name],
        )
        self.db.execute("COMMIT")
        return cursor.lastrowid

    def add_record(self, category: Category, start: datetime, end: datetime):
        """Adds a record to the database."""
        cursor = self.db.execute(
            """
            INSERT INTO Records (category_id, start, end, duration)
                VALUES (?, ?, ?, ?)
            """,
            [category.id, start, end, (end - start).total_seconds()],
        )
        self.db.execute("COMMIT")
        return cursor.lastrowid

    def get_categories(self) -> CategoryManager:
        """Fetches the categories from the database."""
        categories = self.db.execute(
            """
            SELECT name, id
            FROM Categories
            """
        ).fetchall()
        cat_mngr = CategoryManager()
        for data in categories:
            cat_mngr.recreate_existing(data[1], data[0], self.get_duration(data[1]))
        return cat_mngr

    def get_duration(self, category_id) -> float:
        """Fetches the complete duration for the given category"""
        duration = self.db.execute(
            """
            select SUM(Records.duration)
            FROM Records
            WHERE Records.category_id == ?
            """,
            [category_id],
        ).fetchone()[0]
        return duration if duration else 0.0

    def _open_db(self):
        """Opens a connection to the database. If the first time,
        also creates the tables."""
        if not os.path.exists(self._filepath):
            if not os.path.isdir(os.path.dirname(self._filepath)):
                os.mkdir(os.path.dirname(self._filepath))
            self.db = sqlite3.connect(self._filepath)
            self._create_tables()
        else:
            self.db = sqlite3.connect(self._filepath)

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
                duration FLOAT,
                FOREIGN KEY (category_id) REFERENCES Categories(id)
            )
            """
        )

    def close(self):
        self.db.close()
        if False:  # Debugging
            if os.path.exists(DATA_FOLDER_PATH):
                os.remove(DATA_FOLDER_PATH)

    def clear_database(self):
        self.db = None
        pass
