from datetime import date, datetime

from app.messages.model.consts import DATE_FORMAT
from app.model.enums import Category, TaskPriority, TaskStatus


class Task:
    """Основная бизнес сущность с которой будут выполняться все CRUD операции"""

    __slots__ = (
        "id",
        "title",
        "description",
        "category",
        "due_date",
        "priority",
        "status",
    )

    def __init__(
        self, id, title, description, category, due_date, priority, status=TaskStatus.INCOMPLETE
    ) -> None:
        self.id = id
        self.title: str = title
        self.description: str = description
        self.category: Category = Category(category)
        self.due_date: date = datetime.strptime(due_date, DATE_FORMAT).date()
        self.priority: TaskPriority = TaskPriority(priority)
        self.status: TaskStatus = TaskStatus(status)

    def __str__(self):
        """
        Метод для вывода информации о задаче в удобном виде
        """
        return (
            f"Задача №{self.id}\nНазвание: {self.title}\nОписание:  {self.description}\n"
            f"Категория: {self.category.value}\nDeadline: {self.due_date}\n"
            f"Приоритет: {self.priority.value}\nСтатус выдачи: {self.status.value}\n"
        )

    def to_dict(self):
        """
        Метод для преобразования экземпляра задачи в словарь так как json не умеет
        работать с классом Enum и datetime по умолчанию
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category.value,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "priority": self.priority.value,
            "status": self.status.value,
        }
