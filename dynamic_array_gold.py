"""ЛР1. Настраиваемый рост по формуле int(capacity * factor) + 1."""

import math
from dynamic_array import DynamicArray


class DynamicArrayGold(DynamicArray):
    def __init__(self, growth_factor=2.0):
        if isinstance(growth_factor, bool) or not isinstance(growth_factor, (int, float)):
            raise TypeError("Growth factor must be a number")
        if not math.isfinite(growth_factor) or growth_factor <= 1:
            raise ValueError("Growth factor must be finite and greater than 1")
        super().__init__()
        self._growth_factor = growth_factor

    def _resize(self, new_capacity=None):
        if new_capacity is None:
            new_capacity = int(self._capacity * self._growth_factor) + 1
        super()._resize(new_capacity)

    def _grow(self):
        # Одна стратегия роста и для append, и для insert.
        self._resize()
