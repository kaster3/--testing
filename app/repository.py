from enum import Enum

from app.model import Category, Task, TaskStatus
from app.storage import TaskStorage


class TaskRepository:
    """
    Класс TaskRepository предназначен для прямого выполнения CRUD операций, а также работает
    с хранилищем задач, сохраняя туда данные и вытаскивая

    Args:
        self.storage: Класс хранилище
        self.tasks: Список задач, загруженных из json файла
    """

    def __init__(self, storage: TaskStorage) -> None:
        self.storage: TaskStorage = storage
        self.tasks: list[Task | None] = self.storage.load_task_json()

    def get_all_tasks(self) -> list[Task | None]:
        return self.tasks

    def get_tasks_by_category(self, category: Category) -> list[Task | None]:
        return [task for task in self.tasks if task.category == category]

    def get_tasks_by_status(self, status: TaskStatus) -> list[Task | None]:
        return [task for task in self.tasks if task.status == status]

    def add_task(self, task_data) -> None:
        """
        Метод для добавления новой задачи и ее сохранения на основе полученных параметров,
        id получаем зависимостью от декоратора
        """
        new_task = Task(**task_data)
        self.tasks.append(new_task)
        self.storage.save_task_json(tasks=self.tasks)

    def get_task_by_id(self, task_id: int | None) -> Task | None:
        """
        Метод для получения задачи по ее id
        """
        for task in self.tasks:
            if task.id == task_id:
                return task

    def delete_task(self, task: Task) -> None:
        """
        Метод удаления задачи, которая была найдена предварительно
        """
        self.tasks.remove(task)
        self.storage.save_task_json(tasks=self.tasks)

    def update_task(self, task: Task, updated_data: dict) -> None:
        """
        Метод для изменения полей задачи, новыми данными пользователя
        """
        for key, value in updated_data.items():
            if value:
                setattr(task, key, value)

        self.storage.save_task_json(tasks=self.tasks)

    def search_by_key_word(self, key_word: str) -> list[Task]:
        """
        Метод для поиска задач по ключевому слову
        """

        def get_attr_value(task, attr):
            """Получает значение атрибута, обрабатывая Enum."""
            value = getattr(task, attr, None)
            if isinstance(value, Enum):
                return str(value.value)
            return str(value) if value is not None else ""

        return [
            task
            for task in self.tasks
            if any(
                key_word.lower() in get_attr_value(task, attr).lower() for attr in task.__slots__
            )
        ]
