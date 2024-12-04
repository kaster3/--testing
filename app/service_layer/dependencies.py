import functools
from typing import Callable

from app.model import Task
from app.utils.sort_tasks import sort_tasks


def get_task(func) -> Callable:
    """
    Достаточно полезный декоратор, чтобы сразу получать задачу по ID, как зависимость
    в методах, где это необходимо
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs) -> Callable | None:
        try:
            task_id = int(
                input(
                    f"Введите ID задачи для"
                    f" {'удаления' if func.__name__ == 'delete_task' else 'обновления'}: "
                )
            )
        except ValueError:
            print("\n!!! ID должно быть целым числом !!!\n")
            return
        task: Task = self.repository.get_task_by_id(task_id)
        if task:
            return func(self, task, *args, **kwargs)
        print(f"\nЗадачи с ID {task_id} нет в списке\n")
        return

    return wrapper


def id_generator(func) -> Callable:
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        sorted_tasks = sort_tasks(tasks=self.repository.tasks)
        if sorted_tasks:
            generated_id = sorted_tasks[-1].id + 1
            return func(self, generated_id, *args, **kwargs)
        return func(self, *args, **kwargs)

    return wrapper
