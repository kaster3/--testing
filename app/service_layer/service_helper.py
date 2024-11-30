from datetime import datetime

from app.exceptions import EmptyTitleError, PastTimeError
from app.model import Category, Task, TaskPriority, TaskStatus


class ServiceHelper:
    """
    Сделал этот класс, чтобы разгрузить логическое ветвление Service класса
    """

    @staticmethod
    def user_chosen_category(skip: bool = False) -> Category | None:
        """
        Метод для получения категории по вводу пользователя, если флаг skip передали
        есть возможность пропустить ввод
        """
        try:
            category_choice = int(
                input(
                    f"\nВыберите категорию для задачи:"
                    f"\n1. Работа\n2. Личное\n3. Обучение\n{'4. Пропуск' if skip else ''}"
                    f"\nВведите номер варианта ответа: "
                )
            )
        except ValueError:
            print("\n!!! Вводить нужно цифру !!!\n")
            return

        if category_choice == 1:
            return Category.JOB
        elif category_choice == 2:
            return Category.PERSONAL
        elif category_choice == 3:
            return Category.TRAINING
        elif category_choice == 4:
            return

    @staticmethod
    def user_chosen_status(skip: bool = False) -> TaskStatus | None:
        """
        Метод для получения статуса по вводу пользователя, если флаг skip передали
        есть возможность пропустить ввод
        """
        try:
            status_choice = int(
                input(
                    f"\nВыберите статус для задачи:"
                    f"\n1. Выполнено\n2. Не выполнено\n{'3. Пропуск' if skip else ''}"
                    f"\nВведите номер варианта ответа: "
                )
            )
        except ValueError:
            print("\n!!! Вводить нужно цифру !!!\n")
            return

        if status_choice == 1:
            return TaskStatus.COMPLETED
        elif status_choice == 2:
            return TaskStatus.INCOMPLETE
        elif status_choice == 3:
            return None

    @staticmethod
    def user_chosen_priority(skip: bool = False) -> TaskPriority | None:
        """
        Метод для получения приоритета по вводу пользователя, если флаг skip передали
        есть возможность пропустить ввод
        """
        try:
            priority_choice = int(
                input(
                    f"\nВыберите приоритет для задачи:"
                    f"\n1. Высокий\n2. Средний\n3. Низкий\n{'4. Пропуск' if skip else ''}"
                    f"\nВведите номер варианта ответа: "
                )
            )
        except ValueError:
            print("\n!!! Вводить нужно цифру !!!")
            return

        if priority_choice == 1:
            return TaskPriority.HIGH
        elif priority_choice == 2:
            return TaskPriority.MEDIUM
        elif priority_choice == 3:
            return TaskPriority.LOW
        elif priority_choice == 4:
            return

    def user_updated_data(self, task: Task) -> dict:
        """
        Метод для получения измененных данных по вводу пользователя
        """
        updated_data = dict()

        updated_data["title"] = input(
            f"Текущее название: '{task.title}', изменить? (Введите новое название или пропустите): "
        )
        updated_data["description"] = input(
            f"Текущее описание: '{task.description}', изменить? (Введите новое описание или пропустите): "
        )
        print(f"\nТекущая категория: '{task.category.value}', изменить?")
        category = self.user_chosen_category(skip=True)
        updated_data["due_date"] = input(
            f"Текущий дедлайн: '{task.due_date}', изменить? (Введите новый дедлайн или пропустите): "
        )
        print(f"\nТекущий приоритет: '{task.priority.value}', изменить?")
        priority = self.user_chosen_priority(skip=True)
        print(f"\nТекущий статус: '{task.status.value}', изменить?")
        status = self.user_chosen_status(skip=True)

        updated_data["category"] = category
        updated_data["priority"] = priority
        updated_data["status"] = status

        return updated_data

    @staticmethod
    def user_inputted_word() -> str:
        """
        Метод для получения введенного, ключевого слова от пользователя
        """
        key_word = input("Введите ключевое слово для поиска: ")
        return key_word

    @staticmethod
    def get_main_menu() -> str:
        """
        Статический метод для отображения панели управления и приема выбора пользователя
        """
        print("1. Просмотр задач")
        print("2. Добавление задачи")
        print("3. Изменение задачи")
        print("4. Удаление задачи")
        print("5. Поиск задачи по ключевым слова")
        print("6. Выход\n")

        choice = input("Выберите действие: ")
        return choice

    @staticmethod
    def check_tasks(tasks: list[Task | None]) -> None:
        """
        Проверка наличия задач в списке
        """
        if tasks:
            print("\nЗадачи из списка:\n")
            for task in tasks:
                print(task)
        else:
            print("Задачи не найдены.\n")

    @staticmethod
    def validate_date() -> datetime | None:
        """
        Получаем дату от пользователя и валидируем ее по формату "%Y-%m-%d"
        и делаем невозможным внести дату меньше текущей
        """

        date_format = "%Y-%m-%d"
        input_date = input("Введите дедлайн задачи в формате 'YYYY-MM-DD': ")
        try:
            input_date = datetime.strptime(input_date, date_format)
            current_date = datetime.now().date()
            try:
                if input_date.date() < current_date:
                    raise PastTimeError()
            except PastTimeError:
                print("Ошибка: Дедлайн не может быть в прошлом.\n")
                return
        except ValueError:
            print("Ошибка: Неверный формат даты. Ожидается формат 'YYYY-MM-DD'.\n")
            return
        return input_date

    @staticmethod
    def validate_title() -> str | None:
        """
        Получаем название от пользователя и проверяем его на пустую строку
        """
        title = input("Введите название задачи: ")
        try:
            if not title.strip():
                raise EmptyTitleError()
        except EmptyTitleError:
            print("Ошибка: Название задачи не может быть пустым.\n")
            return
        return title
