from app.messages.service.consts import (
    INPUT_CHOICES,
    INPUT_DESCRIPTION,
    NO_DESCRIPTION,
    SHOW_TASKS_WRONG_INPUT,
)
from app.model import Category, Task, TaskStatus
from app.repository import TaskRepository
from app.service_layer.dependencies import get_task, id_generator
from app.service_layer.service_helper import ServiceHelper


class TaskService:
    """
    Класс service_layer предназначен для управления основной логикой выполнения выбранной
    пользователем операции, ветвление логики, отображения сообщений и вызов соответствующих
    методов у класса, такими как: добавление, удаление, поиск и изменение статуса задач (CRUD)
    через класс TaskRepository

    Args:
        repository (TaskRepository): Нужен для выполнения основных CRUD операций
        service_helper (ServiceHelper): Берет на себя вспомогательные операции, для разгрузки
        сложного ветвления логики Service класса
    """

    def __init__(self, repository: TaskRepository, service_helper: ServiceHelper) -> None:
        self.repository: TaskRepository = repository
        self.service_helper: ServiceHelper = service_helper

    def show_tasks(self) -> None:
        """
        Получение всех задач или по категории через TaskRepository
        """
        choice: str = input(INPUT_CHOICES)
        tasks: list[Task | None] = []
        if choice == "1":
            tasks = self.repository.get_all_tasks()
        elif choice == "2":
            category: Category = self.service_helper.user_chosen_category()
            tasks = self.repository.get_tasks_by_category(category)
        elif choice == "3":
            status: TaskStatus = self.service_helper.user_chosen_status()
            tasks = self.repository.get_tasks_by_status(status)
        else:
            print(SHOW_TASKS_WRONG_INPUT)
            return

        self.service_helper.check_tasks(tasks=tasks)

    @id_generator
    def add_task(self, pk: int = 1) -> None:
        """
        Метод для получения параметров книги от пользователя и передаче их методу
        создания в TaskRepository
        """
        task_data = dict()

        title = self.service_helper.validate_title()
        if not title:
            return
        task_data["description"] = (
            NO_DESCRIPTION if not (answer := input(INPUT_DESCRIPTION).strip()) else answer
        )
        date = self.service_helper.validate_date()
        if not date:
            return
        category = self.service_helper.user_chosen_category()
        if not category:
            return
        priority = self.service_helper.user_chosen_priority()
        if not priority:
            return

        task_data["id"] = pk
        task_data["title"] = title
        task_data["category"] = category
        task_data["due_date"] = date
        task_data["priority"] = priority
        task_data["status"] = TaskStatus.INCOMPLETE

        self.repository.add_task(task_data=task_data)

    @get_task
    def delete_task(self, task: Task | None) -> None:
        """
        Получаем от декоратора Task по id и вызываем метод удаления у TaskRepository,
        если такая задача есть в нашем списке
        """
        self.repository.delete_task(task=task)

    @get_task
    def update_task(self, task: Task | None) -> None:
        """
        Получаем от декоратора Task по id и вызываем метод обновления у TaskRepository,
        если такая задача существует, получив новые данные от ServiceHelper
        """
        updated_data = self.service_helper.user_updated_data(task=task)
        self.repository.update_task(task=task, updated_data=updated_data)

    def search_by_key_word(self) -> None:
        """
        Получаем ключевое слово от пользователя через метод класса ServiceHelper
        и вызываем метод поиска у TaskRepository
        """
        key_word = self.service_helper.user_inputted_word()
        tasks = self.repository.search_by_key_word(key_word=key_word)
        self.service_helper.check_tasks(tasks=tasks)

    def get_choice(self) -> str:
        """
        Метод для получения варианта операции из главного меню
        """
        choice = self.service_helper.get_main_menu()
        return choice
