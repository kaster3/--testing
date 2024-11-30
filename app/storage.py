import json
from datetime import datetime

from app.model.enums import Category, TaskPriority, TaskStatus
from app.model.task import Task
from app.utils import sort_tasks


class TaskStorage:
    """
    Класс Storage предназначен для управления хранением и сохранением задач в формате JSON.

    Args:
        self.storage_file (str): имя файла для хранения задач
    """

    def __init__(self, storage_file: str = "tasks.json") -> None:
        self.storage_file = storage_file

    def save_task_json(self, tasks) -> None:
        """
        Метод для сохранения списка задач в формате JSON в указанный файл или созднание этого файла,
        при его отсутствие
        """
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in tasks], file, ensure_ascii=False, indent=4)
        print("\nИзменения сохранены в файл.\n")

    def load_task_json(self) -> list[Task | None]:
        """
        Метод для загрузки задач из файла JSON и преобразования их в список моделей Task
        """
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                tasks_data = json.load(file)

                # Преобразование словаря в модель Book и создание списка книг
                # Возможно выглядит сложно потому, что обязательно нужно привести статус в Enum
                unsorted_tasks: list[Task | None] = [
                    Task(
                        **{
                            **data,
                            "category": Category.from_value(data["category"]),
                            "priority": TaskPriority.from_value(data["priority"]),
                            "status": TaskStatus.from_value(data["status"]),
                            "due_date": (
                                datetime.strptime(data["due_date"], "%Y-%m-%d").date()
                                if "due_date" in data
                                else None
                            ),
                        }
                    )
                    for data in tasks_data
                ]

                return sort_tasks(tasks=unsorted_tasks)

        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Пока ваш файл пуст\n")
            return []
        except KeyError as exc:
            print(f"Ошибка преобразования категории/приоритета/статуса/даты задачи: {exc}")
            return []
