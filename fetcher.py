
import requests
import random
import re

SIZE_5_5 = 0
SIZE_10_10 = 1
SIZE_15_15 = 2
SIZE_20_20 = 3
SIZE_25_25 = 4


def get_random_nonogram(size=None):
    if size is None:
        size = random.choice([SIZE_5_5, SIZE_10_10, SIZE_15_15, SIZE_20_20, SIZE_25_25])

    page = __get_nonogram_page(size)
    task = __get_raw_task(page)
    return __convert_raw_task_to_nonogram(task)


def __get_nonogram_page(size):
    return requests.get("https://www.puzzle-nonograms.com/", {"size": size}).content


def __get_raw_task(page):
    return re.search(b"var task = '([0-9./]+)'", page).group(1).decode('ascii')


def __convert_raw_task_to_nonogram(task):
    all_constraints = tuple(tuple(int(n) for n in group.split('.')) for group in task.split('/'))
    return (
        tuple(all_constraints[:int(len(all_constraints)/2)]),
        tuple(all_constraints[int(len(all_constraints)/2):])
    )


