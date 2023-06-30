"""Python 3.8 list_resize implementation"""
from rich import print

NULL = ...
Py_SSIZE_MAX = 2 ** 31
PyExc_OverflowError = OverflowError

information = {}


class PyListObject:
    def __init__(self):
        self.ob_base = list  # for fun
        self.ob_size = 0
        self.ob_item = []
        self.allocated = 0

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(ob_size={self.ob_size}, "
            f"ob_item={self.ob_item}, "
            f"allocated={self.allocated})"
        )


def PyList_GET_SIZE(self: PyListObject):
    """Return the `len` of self"""
    assert isinstance(self, PyListObject)
    return self.ob_size


def PyList_SET_ITEM(self: PyListObject, n: int, v: object):
    self.ob_item[n] = v


def PyErr_SetString(exception, msg):
    raise exception(msg)


def PyErr_NoMemory():
    PyErr_SetString(MemoryError, "No Memory")


def PyMem_Reaclloc(new_allocated_bytes, self):
    return self.ob_item + ['*'] * (new_allocated_bytes - self.ob_size)


def list_resize(self: PyListObject, newsize: int) -> int:
    allocated = self.allocated

    # Bypass realloc()
    if allocated >= newsize >= (allocated >> 1):
        assert self.ob_item != NULL or newsize == 0
        self.ob_size = newsize
        return 0

    new_allocated = newsize + (newsize >> 3) + (3 if newsize < 9 else 6)

    if new_allocated > Py_SSIZE_MAX / 1:  # assume PyObject pointer is 1 byte
        PyErr_NoMemory()
        return -1

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
    information[self.ob_size] = new_allocated - allocated
    return 0


def app1(self: PyListObject, v: object):
    n = PyList_GET_SIZE(self)
    assert v != NULL

    if n == Py_SSIZE_MAX:
        PyErr_SetString(PyExc_OverflowError,
                        "cannot add more objects to list")
        return -1

    if list_resize(self, n + 1) < 0:
        return -1

    PyList_SET_ITEM(self, n, v)
    return 0


def list_append(self: PyListObject, obj: object):
    if app1(self, obj) == 0:
        return None
    return NULL


lst = PyListObject()
print(lst)
for num in range(1, 128):
    list_append(lst, num)
    if num < 9:
        print(lst)

print(information)
