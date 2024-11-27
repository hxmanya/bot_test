import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_table(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS homeworks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                group_name TEXT,
                homework_number INTEGER,
                github_link TEXT
            )
        ''')
        conn.commit()

    def save_homework(self, name, group_name, homework_number, github_link):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''
                INSERT INTO homeworks 
                (name, group_name, homework_number, github_link) 
                VALUES (?, ?, ?, ?)
            ''', (name, group_name, homework_number, github_link))
            conn.commit()