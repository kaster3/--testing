from enum import Enum


class Category(Enum):
    """
    Клас представляющий категорию задачи (Работа, Личное, Обучение), для более
     удобного взаимодействия и уменьшения шанса на ошибку
    """

    JOB = "Работа"
    PERSONAL = "Личное"
    TRAINING = "Обучение"

    @staticmethod
    def from_value(value: str) -> "Category":
        """
        Метод для получения категории задачи по его значению, для того чтобы json
        корректно работал с Enum
        """
        for status in Category:
            if status.value == value:
                return status
