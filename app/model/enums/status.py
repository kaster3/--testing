from enum import Enum


class TaskStatus(Enum):
    """
    Клас представляющий статус задачи (Выполнена, Не выполнена), для более удобного взаимодействия
    и уменьшения шанса на ошибку
    """

    COMPLETED = "Выполнено"
    INCOMPLETE = "Не выполнена"

    @staticmethod
    def from_value(value: str) -> "TaskStatus":
        """
        Метод для получения статуса задачи по его значению, для того чтобы json
        корректно работал с Enum
        """
        for status in TaskStatus:
            if status.value == value:
                return status
        return TaskStatus.COMPLETED
