from repository import TaskRepository
from service_layer import TaskService
from service_layer.service_helper import ServiceHelper
from storage import TaskStorage


def main() -> None:
    """
    Главный цикл приложения, который обрабатывает взаимодействие с пользователем и вызывает
    соответствующие методы у класса TaskService, выполняя основную бизнес логику
    """
    storage = TaskStorage()
    repository = TaskRepository(storage=storage)
    service_helper = ServiceHelper()
    service = TaskService(repository=repository, service_helper=service_helper)

    while True:
        choice = service.get_choice()

        if choice == "1":
            service.show_tasks()

        elif choice == "2":
            service.add_task()

        elif choice == "3":
            service.update_task()

        elif choice == "4":
            service.delete_task()

        elif choice == "5":
            service.search_by_key_word()

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Выбери число от 1 до 6 включительно.\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(
            f"Кажется это операция не работает,"
            f" свяжитесь с разработчиком.\n{exc.__class__.__name__} -> {exc}"
        )
