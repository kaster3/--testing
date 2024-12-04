from app.messages.main.consts import MAIN_EXIT, WRONG_INPUT
from app.messages.main.message_formatter import main_exception
from app.data_accesor_layer.repository import TaskRepository
from app.service_layer import TaskService
from app.service_layer.service_helper import ServiceHelper
from app.storage_layer.storage import TaskStorage


def main(service: TaskService) -> None:
    """
    Главный цикл приложения, который обрабатывает взаимодействие с пользователем и вызывает
    соответствующие методы у класса TaskService, выполняя основную бизнес логику
    """

    choices = {
        "1": service.show_tasks,
        "2": service.add_task,
        "3": service.update_task,
        "4": service.delete_task,
        "5": service.search_by_key_word,
        "6": lambda: print(MAIN_EXIT),
    }

    while True:
        choice = service.get_choice()
        choices.get(choice, lambda: print(WRONG_INPUT))()
        if choice == "6":
            break


if __name__ == "__main__":
    storage = TaskStorage()
    repository = TaskRepository(storage=storage)
    service_helper = ServiceHelper()
    service = TaskService(repository=repository, service_helper=service_helper)
    try:
        main(service=service)
    except Exception as exc:
        print(main_exception(exc=exc))
