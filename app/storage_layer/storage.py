import json

from app.messages.storage.consts import EMPTY_FILE, SAVE_CHANGES
from app.messages.storage.message_formatter import format_key_error_message
from app.model.task import Task
from app.utils.sort_tasks import sort_tasks


class TaskStorage:
    """
    Класс Storage предназначен для управления хранением и сохранением задач в формате JSON.

    Args:
        self.storage_file (str): имя файла для хранения задач
    """

    default_name = "storage_layer/tasks.json"

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

                unsorted_tasks: list[Task | None] = [Task(**data) for data in tasks_data]

                # Сортируем по id, на случай, если в файле сделали перестановку книг, будет
                # неверно формироваться id новой книги в этом случает т.к.
                # правило list(Task...)[-1]["id]
                return sort_tasks(tasks=unsorted_tasks)

        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(EMPTY_FILE)
            return []
        except KeyError as exc:
            print(format_key_error_message(exc=exc))
            return []
