from datetime import datetime

import pytest
from syrupy import SnapshotAssertion, snapshot

from app.model import Category, TaskPriority, TaskStatus


class TestTaskRepository:

    def test_get_all_tasks(self, repository_with_tasks, snapshot: SnapshotAssertion):
        all_tasks = repository_with_tasks.get_all_tasks()
        assert len(all_tasks) == 4
        snapshot.assert_match([task.to_dict() for task in all_tasks])

    def test_get_tasks_by_category(self, repository_with_tasks):
        category_tasks = repository_with_tasks.get_tasks_by_category(category=Category.JOB)
        assert len(category_tasks) == 2

    @pytest.mark.parametrize(
        "status, result",
        [
            (TaskStatus.INCOMPLETE, 3),
            (TaskStatus.COMPLETED, 1),
        ],
    )
    def test_get_tasks_by_status(self, status, result, repository_with_tasks, snapshot: SnapshotAssertion):
        tasks = repository_with_tasks.get_tasks_by_status(status=status)
        assert len(tasks) == result
        snapshot.assert_match([task.to_dict() for task in tasks])

    def test_add_task(self, repository, mock_storage, snapshot: SnapshotAssertion):
        task_data_1 = {
            "id": 5,
            "title": "New Task",
            "description": "This is a new task",
            "category": Category.PERSONAL,
            "due_date": datetime.strptime("2025-12-23", "%Y-%m-%d"),
            "priority": TaskPriority.HIGH,
            "status": TaskStatus.INCOMPLETE,
        }
        task_data_2 = {
            "id": 6,
            "title": "Task 2",
            "description": "This is task 2",
            "category": Category.TRAINING,
            "due_date": datetime.strptime("2025-12-23", "%Y-%m-%d"),
            "priority": TaskPriority.LOW,
            "status": TaskStatus.INCOMPLETE,
        }
        repository.add_task(task_data=task_data_1)
        repository.add_task(task_data=task_data_2)

        all_tasks = repository.get_all_tasks()
        assert len(all_tasks) == 2
        snapshot.assert_match([task.to_dict() for task in all_tasks])
        assert mock_storage.save_task_json.call_count == 2

    @pytest.mark.parametrize("task_id", [1, 2, 3])
    def test_get_task_by_id(self, repository_with_tasks, task_id, snapshot):
        task = repository_with_tasks.get_task_by_id(task_id)
        snapshot.assert_match(task.to_dict())

    def test_delete_task(self, repository_with_tasks, snapshot):
        tasks = repository_with_tasks.get_all_tasks()
        assert len(tasks) == 4
        repository_with_tasks.delete_task(task=tasks[0])
        assert len(tasks) == 3
        snapshot.assert_match([task.to_dict() for task in tasks])

    def test_update_task(self, repository_with_tasks, snapshot, mock_storage):
        task = repository_with_tasks.get_task_by_id(task_id=1)
        updated_data = {
            "title": "Updated Task",
            "description": "This is an updated task",
            "category": Category.PERSONAL,
            "due_date": datetime.strptime("2025-12-23", "%Y-%m-%d"),
            "priority": TaskPriority.HIGH,
            "status": TaskStatus.INCOMPLETE,
        }
        repository_with_tasks.update_task(task=task, updated_data=updated_data)
        updated_task = repository_with_tasks.get_task_by_id(task_id=1)
        snapshot.assert_match(updated_task.to_dict())
        assert mock_storage.save_task_json.call_count == 5

    @pytest.mark.parametrize(
        "key_word, result",
        [
            ("Task", 4),
            ("Высокий", 2),
            ("Описание", 1),
            ("Работа", 2),
            ("Не выполнена", 3),
            ("Выполнено", 1),
        ],
    )
    def test_search_by_key_word(self, key_word, result, repository_with_tasks, snapshot):
        tasks = repository_with_tasks.search_by_key_word(key_word=key_word)
        assert len(tasks) == result
        snapshot.assert_match([task.to_dict() for task in tasks])
