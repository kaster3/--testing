from datetime import datetime

import pytest

from app.model import Category, Task, TaskPriority, TaskStatus
from app.repository import TaskRepository
from app.service_layer import TaskService
from app.service_layer.service_helper import ServiceHelper
from tests.fixtures.storage import created_tasks


@pytest.fixture()
def service(mock_repository: TaskRepository, mock_service_helper: ServiceHelper) -> TaskService:
    return TaskService(repository=mock_repository, service_helper=mock_service_helper)


@pytest.fixture()
def mock_repository(mocker, created_tasks):
    mock_repository = mocker.MagicMock(spec=TaskRepository)
    mock_repository.get_all_tasks.return_value = created_tasks
    mock_repository.get_tasks_by_category.return_value = [
        task for task in created_tasks if task.category == Category.JOB
    ]
    mock_repository.get_tasks_by_status.return_value = [
        task for task in created_tasks if task.status == TaskStatus.COMPLETED
    ]
    return mock_repository


@pytest.fixture()
def mock_service_helper(mocker):
    mock_service_helper = mocker.MagicMock(spec=ServiceHelper)
    mock_service_helper.user_chosen_category.return_value = Category.JOB
    mock_service_helper.user_chosen_status.return_value = TaskStatus.COMPLETED
    return mock_service_helper


@pytest.fixture()
def created_task():
    task_1 = Task(
        id=1,
        title="test title 1",
        description="test description 1",
        category=Category.PERSONAL,
        due_date=datetime.strptime("2026-12-20", "%Y-%m-%d"),
        priority=TaskPriority.HIGH,
        status=TaskStatus.INCOMPLETE,
    )
    return task_1
