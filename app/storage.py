import json
from datetime import datetime

from app.messages.storage.consts import EMPTY_FILE, SAVE_CHANGES
from app.messages.storage.message_formatter import format_key_error_message
from app.model.enums import Category, TaskPriority, TaskStatus
from app.model.task import Task
from app.utils import sort_tasks


class TaskStorage:
    """
    Класс Storage предназначен для управления хранением и сохранением задач в формате JSON.

    Args:
        self.storage_file (str): имя файла для хранения задач
    """

    default_name = "tasks.json"

    def __init__(self, storage_file: str = default_name) -> None:
        self.storage_file = storage_file

    def save_task_json(self, tasks) -> None:
        """
        Метод для сохранения списка задач в формате JSON в указанный файл или созднание этого файла,
        при его отсутствие
        """
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in tasks], file, ensure_ascii=False, indent=4)
        print(SAVE_CHANGES)

    def load_task_json(self) -> list[Task | None]:
        """
        Метод для загрузки задач из файла JSON и преобразования их в список моделей Task
        """
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                tasks_data = json.load(file)

                # Преобразование словаря в модель Book и создание списка книг
                # Возможно выглядит сложно потому, что обязательно нужно привести статус,
                # категорию и приоритет в Enum, а также дату в datetime
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
            print(EMPTY_FILE)
            return []
        except KeyError as exc:
            print(format_key_error_message(exc=exc))
            return []
