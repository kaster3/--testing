from app.model import Task


def sort_tasks(tasks: list[Task | None]) -> list[Task | None]:
    """
    Сортировка задач по id, на случай, если книги в файле были переставлены,
    так как будет генерироваться неправильный id, он генерируется: books[-1] + 1
    и просто для отсортированной выдачи товара
    """
    return sorted(tasks, key=lambda task: task.id)
