"""Python 3.11 list_resize implementation"""
from math import floor

NULL = ...
Py_SSIZE_MAX = 2 ** 31


class PyListObject:
    def __init__(self):
        self.ob_base = list  # for fun
        self.ob_size = 0
        self.ob_item = []
        self.allocated = 0

    def append(self, obj: object) -> None:
        return list_append(self, obj)

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(ob_size={self.ob_size}, "
            f"ob_item={self.ob_item}, "
            f"allocated={self.allocated})"
        )


def PyErr_SetString(exception, msg):
    raise exception(msg)


def PyErr_NoMemory():
    PyErr_SetString(MemoryError, "No Memory")


def PyList_SET_ITEM(self: PyListObject, n: int, v: object):
    self.ob_item[n] = v


def PyMem_Reaclloc(new_allocated_bytes, self):
    return self.ob_item + ['*'] * (new_allocated_bytes - self.ob_size)


def list_resize(self: PyListObject, newsize: int) -> int:
    allocated = self.allocated

    # Bypass realloc()
    if allocated >= newsize >= floor(allocated >> 1):
        assert self.ob_item != NULL or newsize == 0
        self.ob_size = newsize
        return 0

    new_allocated = (newsize + floor(newsize >> 3) + 6) & (~3)

    if (newsize - self.ob_size) > (new_allocated - newsize):
        new_allocated = (newsize + 3) & (~3)

    if newsize == 0:
        new_allocated = 0

    if new_allocated <= Py_SSIZE_MAX / 1:
        new_allocated_bytes = new_allocated * 1
        items = PyMem_Reaclloc(new_allocated_bytes, self)
    else:
        items = NULL

    if items == NULL:
        PyErr_NoMemory()
        return -1

    self.ob_item = items
    self.ob_size = newsize
    self.allocated = new_allocated
    return 0


def _PyList_AppendTakeRefResize(self, newitem):
    len_ = self.ob_size
    assert self.allocated == -1 or self.allocated == len_
    if list_resize(self, len_ + 1) < 0:
        return -1
    PyList_SET_ITEM(self, len_, newitem)
    return 0


def _PyList_AppendTakeRef(self, newitem):
    assert self != NULL and newitem != NULL
    assert isinstance(self, PyListObject)
    len_ = self.ob_size
    allocated = self.allocated
    assert len_ + 1 < Py_SSIZE_MAX
    if allocated > len_:
        self.ob_size = len_ + 1
        PyList_SET_ITEM(self, len_, newitem)
        return 0
    return _PyList_AppendTakeRefResize(self, newitem)


def list_append(self, obj):
    if _PyList_AppendTakeRef(self, obj) < 0:
        return NULL
    return None


lst = PyListObject()
for num in range(16):
    lst.append(num)

lst.append("Mahdi")
