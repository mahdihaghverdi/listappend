import csv
from collections import Counter
from sys import getsizeof

import matplotlib.pyplot as plt

from impls.listimpltheight import PyListObject as PyListObject38
from impls.listimplthele import PyListObject as PyListObject311


def list_size(List, size: int):
    """Add `size` objects to the list"""
    lst = List()
    info_list = [(lst.ob_size, getsizeof(lst.ob_item))]
    for num in range(size):
        lst.append(num)
        info_list.append((lst.ob_size, getsizeof(lst.ob_item)))
    return info_list


with open('./stats/3.8cpystat.csv', newline='') as f:
    reader = csv.DictReader(f)
    cpy_info = {}
    for row in reader:
        cpy_info[int(row['list_size'])] = int(row['getsizeof'])

impl_info = list_size(PyListObject38, 126)
impl_counter = Counter([inf[1] for inf in impl_info])
impl_sorted_counter = dict(sorted(impl_counter.items()))
impl_sizes = impl_sorted_counter.keys()
impl_counts = impl_sorted_counter.values()

cpy_counter = Counter([inf[1] for inf in cpy_info.items()])
cpy_sorted_counter = dict(sorted(cpy_counter.items()))
cpy_sizes = cpy_sorted_counter.keys()
cpy_counts = cpy_sorted_counter.values()

with open('./stats/3.11cpystat.csv', newline='') as f:
    reader = csv.DictReader(f)
    cpy_info = {}
    for row in reader:
        cpy_info[int(row['list_size'])] = int(row['getsizeof'])

impl_info_311 = list_size(PyListObject311, 126)
impl_counter = Counter([inf[1] for inf in impl_info_311])
impl_sorted_counter = dict(sorted(impl_counter.items()))
impl_sizes_311 = impl_sorted_counter.keys()
impl_counts_311 = impl_sorted_counter.values()

cpy_counter = Counter([inf[1] for inf in cpy_info.items()])
cpy_sorted_counter = dict(sorted(cpy_counter.items()))
cpy_sizes_311 = cpy_sorted_counter.keys()
cpy_counts_311 = cpy_sorted_counter.values()

plt.figure(figsize=(10, 6))
plt.plot(
    # impl_sizes, impl_counts, '-',
    # impl_sizes_311, impl_counts_311,
    cpy_sizes, cpy_counts, '-.',
    cpy_sizes_311, cpy_counts_311,


)
plt.xlabel('Size in bytes.')
plt.ylabel('This size for how many of items in list.')
plt.title('List size growth according to its len')
# plt.xticks(list(cpy_sizes_311), list(cpy_sizes_311))
# plt.yticks(list(cpy_counts_311), list(cpy_counts_311))

plt.savefig('size_growth.png')
