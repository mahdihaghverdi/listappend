"""Python 3.8 list_resize implementation"""


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
