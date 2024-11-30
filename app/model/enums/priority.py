from enum import Enum


class TaskPriority(Enum):
    """
    Клас представляющий приоритет задачи (Высокий, Средний, Низкий), для более
    удобного взаимодействия и уменьшения шанса на ошибку
    """

    HIGH = "Высокий"
    MEDIUM = "Средний"
    LOW = "Низкий"

    @staticmethod
    def from_value(value: str) -> "TaskPriority":
        """
        Метод для получения приоритета задачи по его значению, для того чтобы
        json корректно работал с Enum
        """
        for status in TaskPriority:
            if status.value == value:
                return status
