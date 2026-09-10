"""ЛР1. Статический массив на базе ctypes, без встроенных контейнеров."""

import ctypes
import operator


class StaticArray:
    def __init__(self, capacity: int):
        capacity = operator.index(capacity)
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._size = 0
        self._array = (ctypes.py_object * capacity)()

    @property
    def capacity(self):
        return self._capacity

    def _check_index(self, index, *, insertion=False):
        index = operator.index(index)
        upper = self._size if insertion else self._size - 1
        if not 0 <= index <= upper:
            raise IndexError("Index out of bounds")
        return index

    def get(self, index):
        """Чтение существующего элемента: O(1)."""
        return self._array[self._check_index(index)]

    def set(self, index, value):
        """Изменение существующего элемента: O(1)."""
        self._array[self._check_index(index)] = value

    def append(self, value):
        """Добавление без расширения: O(1)."""
        if self._size == self._capacity:
            raise OverflowError("Array is full")
        self._array[self._size] = value
        self._size += 1

    def __len__(self):
        return self._size

    def __iter__(self):
        for i in range(self._size):
            yield self._array[i]

    def __str__(self):
        return "[" + ", ".join(str(value) for value in self) + "]"
