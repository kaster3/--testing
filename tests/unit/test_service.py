from unittest.mock import patch

import pytest

from app.model import Category, TaskStatus
from app.data_accesor_layer.repository import TaskRepository
from app.service_layer import TaskService
from app.service_layer.service_helper import ServiceHelper


class TestService:
    @pytest.mark.parametrize(
        "choice, expected_method",
        [
            ("1", "get_all_tasks"),
            ("2", "get_tasks_by_category"),
            ("3", "get_tasks_by_status"),
        ],
    )
    def test_show_tasks(
        self,
        choice: int,
        expected_method: str,
        service: TaskService,
        mock_repository: TaskRepository,
        mock_service_helper: ServiceHelper,
    ) -> None:
        with patch("builtins.input", return_value=choice):
            service.show_tasks()

            if expected_method == "get_all_tasks":
                mock_repository.get_all_tasks.assert_called_once()
            elif expected_method == "get_tasks_by_category":
                mock_service_helper.user_chosen_category.assert_called_once()
                mock_repository.get_tasks_by_category.assert_called_once_with(Category.JOB)
            elif expected_method == "get_tasks_by_status":
                mock_service_helper.user_chosen_status.assert_called_once()
                mock_repository.get_tasks_by_status.assert_called_once_with(TaskStatus.COMPLETED)

            tasks = (
                mock_repository.get_all_tasks()
                if choice == "1"
                else (
                    mock_repository.get_tasks_by_category(Category.JOB)
                    if choice == "2"
                    else mock_repository.get_tasks_by_status(TaskStatus.COMPLETED)
                )
            )
            mock_service_helper.check_tasks.assert_called_once_with(tasks=tasks)
