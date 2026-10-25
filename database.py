
import sqlite3
from datetime import datetime
from pathlib import Path

DB_NAME = Path(__file__).resolve().parent / "nexus.db"


def connect_db(db_path=DB_NAME):
    """Abre una conexión con la base de datos."""
    return sqlite3.connect(str(db_path))


def initialize_db(db_path=DB_NAME):
    """Crea la tabla de tareas si todavía no existe."""
    with connect_db(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                created_at TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
                    CHECK (completed IN (0, 1))
            )
        """)


def add_task(title, category="Personal", db_path=DB_NAME):
    """Guarda una nueva tarea."""
    title = title.strip()
    category = category.strip()

    if not title:
        raise ValueError("El título no puede estar vacío.")

    if not category:
        raise ValueError("La categoría no puede estar vacía.")

    with connect_db(db_path) as conn:
        cursor = conn.execute("""
            INSERT INTO tasks (title, category, created_at)
            VALUES (?, ?, ?)
        """, (
            title,
            category,
            datetime.now().isoformat(timespec="minutes"),
        ))

        return cursor.lastrowid


def get_tasks(db_path=DB_NAME):
    """Devuelve todas las tareas, de más recientes a más antiguas."""
    with connect_db(db_path) as conn:
        return conn.execute("""
            SELECT id, title, category, created_at, completed
            FROM tasks
            ORDER BY completed ASC, id DESC
        """).fetchall()


def toggle_task(task_id, completed, db_path=DB_NAME):
    """Marca una tarea como completada o pendiente."""
    if completed not in (True, False, 0, 1):
        raise ValueError("El estado debe ser True o False.")

    with connect_db(db_path) as conn:
        cursor = conn.execute("""
            UPDATE tasks
            SET completed = ?
            WHERE id = ?
        """, (int(completed), task_id))

        return cursor.rowcount > 0


def delete_task(task_id, db_path=DB_NAME):
    """Elimina una tarea por su identificador."""
    with connect_db(db_path) as conn:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )

        return cursor.rowcount > 0
