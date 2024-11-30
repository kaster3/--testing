from datetime import datetime

from app.model import Task


def sort_tasks(tasks: list[Task | None]) -> list[Task | None]:
    """
    Сортировка задач по id, на случай, если книги в файле были переставлены,
    так как будет генерироваться неправильный id, он генерируется: books[-1] + 1
    и просто для отсортированной выдачи товара
    """
    return sorted(tasks, key=lambda task: task.id)


def validate_date(date_string: str) -> bool:
    date_format = "%Y-%m-%d"
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False
