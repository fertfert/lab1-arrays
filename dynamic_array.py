"""ЛР1. Динамический массив с удвоением и сжатием ёмкости."""

import ctypes
import operator
from static_array import StaticArray


class DynamicArray(StaticArray):
    def __init__(self):
        super().__init__(1)

    def _make_array(self, capacity):
        return (ctypes.py_object * capacity)()

    def _resize(self, new_capacity):
        new_capacity = operator.index(new_capacity)
        if new_capacity < max(1, self._size):
            raise ValueError("Capacity must fit all elements and be positive")
        new_array = self._make_array(new_capacity)
        for i in range(self._size):
            new_array[i] = self._array[i]
        self._array = new_array
        self._capacity = new_capacity

    def _grow(self):
        self._resize(2 * self._capacity)

    def append(self, value):
        """O(1) амортизированно, O(n) при расширении."""
        if self._size == self._capacity:
            self._grow()
        super().append(value)

    def insert(self, index, value):
        """Вставляет перед index; index == len(self) допустим. O(n)."""
        index = self._check_index(index, insertion=True)
        if self._size == self._capacity:
            self._grow()
        # Сдвиг справа налево сохраняет ещё не скопированные элементы.
        for i in range(self._size, index, -1):
            self._array[i] = self._array[i - 1]
        self._array[index] = value
        self._size += 1

    def remove(self, index):
        """Удаляет по индексу. Сжатие при заполнении не более четверти."""
        index = self._check_index(index)
        for i in range(index, self._size - 1):
            self._array[i] = self._array[i + 1]
        self._size -= 1
        # Убираем ссылку на объект в освободившейся ячейке.
        self._array[self._size] = None
        if self._capacity > 1 and self._size <= self._capacity // 4:
            self._resize(max(1, self._capacity // 2))

    def find(self, value):
        """Индекс первого совпадения или None. O(n)."""
        for i in range(self._size):
            if self._array[i] == value:
                return i
        return None

    def binary_search(self, value):
        """Индекс совпадения или None. Требует сортировки по возрастанию.

        Порядок не проверяется, чтобы сохранить O(log n).
        """
        left, right = 0, self._size - 1
        while left <= right:
            middle = (left + right) // 2
            current = self._array[middle]
            if current == value:
                return middle
            if current < value:
                left = middle + 1
            else:
                right = middle - 1
        return None
