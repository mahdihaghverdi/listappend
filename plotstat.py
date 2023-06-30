import csv
from collections import Counter
from sys import getsizeof

import matplotlib.pyplot as plt

from listimpltheight import PyListObject


def list_size(size: int):
    """Add `size` objects to the list"""
    lst = PyListObject()
    info_list = [(lst.ob_size, getsizeof(lst.ob_item))]
    for num in range(size):
        lst.append(num)
        info_list.append((lst.ob_size, getsizeof(lst.ob_item)))
    return info_list


with open('3.8cpystatall.csv', newline='') as f:
    reader = csv.DictReader(f)
    cpy_info = {}
    for row in reader:
        cpy_info[int(row['list_size'])] = int(row['getsizeof'])

impl_info = list_size(126)
impl_counter = Counter([inf[1] for inf in impl_info])
impl_sorted_counter = dict(sorted(impl_counter.items()))
impl_sizes = impl_sorted_counter.keys()
impl_counts = impl_sorted_counter.values()

cpy_counter = Counter([inf[1] for inf in cpy_info.items()])
cpy_sorted_counter = dict(sorted(cpy_counter.items()))
cpy_sizes = cpy_sorted_counter.keys()
cpy_counts = cpy_sorted_counter.values()

plt.figure(figsize=(10, 6))
plt.plot(
    impl_sizes, impl_counts, '-',
    # cpy_sizes, cpy_counts, '--',
)
plt.xlabel('Size in bytes.')
plt.ylabel('This size for how many of items in list.')
plt.title('List size growth according to its len')
plt.xticks(list(cpy_sizes), list(cpy_sizes))
plt.yticks(list(cpy_counts), list(cpy_counts))

plt.savefig('size_growth_3.8.png')
