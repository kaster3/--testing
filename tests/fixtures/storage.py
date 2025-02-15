import os

import pytest

from app.model import Category, Task, TaskPriority, TaskStatus
from app.storage_layer.storage import TaskStorage
from tests.messages.storage import TEST_FILE_NAME


@pytest.fixture()
def storage() -> TaskStorage:
    file_name = TEST_FILE_NAME
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
        due_date="2025-12-23",
        priority=TaskPriority.LOW,
        status=TaskStatus.INCOMPLETE,
    )
    return [created_task, task_2]


@pytest.fixture()
def saved_file(storage: TaskStorage, created_tasks):
    storage.save_task_json(created_tasks)
    yield storage
