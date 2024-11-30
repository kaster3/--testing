import os
from datetime import datetime

import pytest

from app.model import Category, Task, TaskPriority, TaskStatus
from app.storage import TaskStorage


@pytest.fixture()
def storage() -> TaskStorage:
    file_name = "test_tasks.json"
    storage = TaskStorage(storage_file=file_name)
    yield storage
    os.remove(file_name)


@pytest.fixture()
def created_tasks(created_task) -> list[Task]:
    task_2 = Task(
        id=2,
        title="test title 2",
        description="test description 2",
        category=Category.JOB,
        due_date=datetime.strptime("2025-12-23", "%Y-%m-%d"),
        priority=TaskPriority.LOW,
        status=TaskStatus.INCOMPLETE,
    )
    return [created_task, task_2]


@pytest.fixture()
def saved_file(storage: TaskStorage, created_tasks):
    storage.save_task_json(created_tasks)
    yield storage
