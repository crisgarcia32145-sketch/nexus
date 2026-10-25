
import pytest

from database import (
    initialize_db,
    add_task,
    get_tasks,
    toggle_task,
    delete_task,
)


@pytest.fixture
def test_db(tmp_path):
    """Crea una base de datos temporal para cada prueba."""
    db_path = tmp_path / "test_nexus.db"
    initialize_db(db_path)
    return db_path


def test_add_and_get_task(test_db):
    task_id = add_task(
        "Aprender Python",
        "Programación",
        test_db,
    )

    tasks = get_tasks(test_db)

    assert len(tasks) == 1
    assert tasks[0][0] == task_id
    assert tasks[0][1] == "Aprender Python"
    assert tasks[0][2] == "Programación"
    assert tasks[0][4] == 0


def test_reject_empty_title(test_db):
    with pytest.raises(ValueError):
        add_task("   ", "Estudios", test_db)

    assert get_tasks(test_db) == []


def test_complete_task(test_db):
    task_id = add_task("Crear NEXUS", "Programación", test_db)

    result = toggle_task(task_id, True, test_db)

    assert result is True
    assert get_tasks(test_db)[0][4] == 1


def test_delete_task(test_db):
    task_id = add_task("Tarea temporal", "Personal", test_db)

    assert delete_task(task_id, test_db) is True
    assert get_tasks(test_db) == []


def test_delete_missing_task(test_db):
    assert delete_task(999, test_db) is False
