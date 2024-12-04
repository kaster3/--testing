import pytest

from app.model import Category, TaskPriority, TaskStatus
from app.data_accesor_layer.repository import TaskRepository


@pytest.fixture()
def repository_with_tasks(repository: TaskRepository):
    task_data_1 = dict(
        id=1,
        title="Task 1",
        description="Описание 1",
        category=Category.JOB,
        due_date="2025-12-23",
        status=TaskStatus.INCOMPLETE,
        priority=TaskPriority.HIGH,
    )
    task_data_2 = dict(
        id=2,
        title="Task 2",
        description="Description 2",
        category=Category.PERSONAL,
        due_date="2025-12-23",
        status=TaskStatus.INCOMPLETE,
        priority=TaskPriority.LOW,
    )
    task_data_3 = dict(
        id=3,
        title="Task 3",
        description="",
        category=Category.TRAINING,
        due_date="2025-12-23",
        status=TaskStatus.COMPLETED,
        priority=TaskPriority.LOW,
    )
    task_data_4 = dict(
        id=4,
        title="Task 4",
        description="Description 4",
        category=Category.JOB,
        due_date="2025-12-23",
        status=TaskStatus.INCOMPLETE,
        priority=TaskPriority.HIGH,
    )

    for task in task_data_1, task_data_2, task_data_3, task_data_4:
        repository.add_task(task_data=task)

    yield repository
    repository.tasks.clear()


@pytest.fixture()
def mock_storage(mocker):
    mock_storage = mocker.MagicMock()
    mock_storage.load_task_json.return_value = []
    return mock_storage


@pytest.fixture()
def repository(mock_storage) -> TaskRepository:
    return TaskRepository(storage=mock_storage)
