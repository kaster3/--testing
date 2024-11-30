import os

from syrupy import SnapshotAssertion

from app.model import Task
from app.storage import TaskStorage


class TestStorage:

    def test_save_task_json(self, created_tasks: list[Task], storage: TaskStorage):
        with open(storage.storage_file, "w", encoding="utf-8") as file:
            assert file.name == "test_tasks.json"
            assert os.path.exists(file.name) is True
            storage.save_task_json(tasks=created_tasks)

    def test_load_task_json(self, saved_file: TaskStorage, snapshot: SnapshotAssertion):
        loaded_tasks = saved_file.load_task_json()
        assert len(loaded_tasks) == 2
        snapshot.assert_match([task.to_dict() for task in loaded_tasks])
