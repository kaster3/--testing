from app.utils import sort_tasks

def test_sort_tasks(created_tasks) -> None:
    unsorted_list = list()
    unsorted_list.append(created_tasks[1])
    unsorted_list.append(created_tasks[0])
    assert unsorted_list[0].id == 2
    assert unsorted_list[1].id == 1
    sorted_list = sort_tasks(unsorted_list)
    assert sorted_list[0].id == 1
    assert sorted_list[1].id == 2
