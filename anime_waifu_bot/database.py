import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            user_id INTEGER,
            img_url TEXT
        )
        """)
        self.connection.commit()

    def add_to_favorites(self, user_id: int, img_url: str):
        self.cursor.execute("INSERT INTO favorites VALUES (?, ?)", (user_id, img_url))
        self.connection.commit()
