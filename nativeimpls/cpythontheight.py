import csv
import pathlib
from sys import getsizeof


def list_size(size: int):
    """Add `size` objects to the list"""
    lst = []
    info_list = [(len(lst), getsizeof(lst))]
    for num in range(size):
        lst.append(num)
        info_list.append((len(lst), getsizeof(lst)))
    return info_list


information = list_size(126)

with open('./stats/3.8cpystat.csv', 'w', newline='') as all_f:
    fieldnames = ['list_size', 'getsizeof']
    writer = csv.DictWriter(all_f, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(
        [
            {'list_size': info[0], 'getsizeof': info[1]}
            for info in information
        ]
    )
