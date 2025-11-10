import sqlite3
from models import Task

class DatabaseManager:
    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time TEXT NOT NULL,
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            conn.commit()

    def add_task(self, task: Task) -> int:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (time, text, created_at)
                VALUES (?, ?, ?)
            ''', (task.time, task.text, task.created_at))
            conn.commit()
            return cursor.lastrowid

    def get_all_tasks(self) -> list[Task]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
            rows = cursor.fetchall()

            tasks = []
            for row in rows:
                task = Task(
                    id=row[0],
                    time=row[1],
                    text=row[2],
                    created_at=row[3]
                )
                tasks.append(task)
            return tasks

    def delete_task(self, task_id: int) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_task(self, task_id: int) -> Task:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()

            if row:
                return Task(
                    id=row[0],
                    time=row[1],
                    text=row[2],
                    created_at=row[3]
                )
            return None