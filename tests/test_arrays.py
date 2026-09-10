import random
import unittest

from static_array import StaticArray
from dynamic_array import DynamicArray
from dynamic_array_gold import DynamicArrayGold


class ArrayTests(unittest.TestCase):
    def test_static(self):
        for capacity in (0, -1):
            with self.assertRaises(ValueError):
                StaticArray(capacity)
        arr = StaticArray(2)
        self.assertEqual(str(arr), "[]")
        with self.assertRaises(IndexError):
            arr.get(0)
        arr.append(None)
        arr.append("hello")
        self.assertIsNone(arr.get(0))
        arr.set(0, 42)
        self.assertEqual(str(arr), "[42, hello]")
        with self.assertRaises(OverflowError):
            arr.append(3)
        for index in (-1, 2, 100):
            with self.assertRaises(IndexError):
                arr.get(index)
            with self.assertRaises(IndexError):
                arr.set(index, 0)
        with self.assertRaises(TypeError):
            arr.get(0.5)

    def test_handout(self):
        arr = DynamicArray()
        for i in range(100):
            arr.append(i)
        self.assertEqual(len(arr), 100)
        self.assertEqual(arr.get(50), 50)
        arr.insert(10, 999)
        self.assertEqual(arr.get(10), 999)
        arr.remove(10)
        self.assertEqual(arr.get(10), 10)
        self.assertEqual(arr.find(50), 50)
        self.assertEqual(arr.binary_search(50), 50)

    def test_search(self):
        arr = DynamicArray()
        self.assertIsNone(arr.find(1))
        self.assertIsNone(arr.binary_search(1))
        for value in (-5, 0, 0, 2, 10):
            arr.append(value)
        self.assertEqual(arr.find(0), 1)
        for value in (-5, 0, 2, 10):
            self.assertEqual(arr.get(arr.binary_search(value)), value)
        for value in (-6, 1, 11):
            self.assertIsNone(arr.find(value))
            self.assertIsNone(arr.binary_search(value))

    def test_growth_shrink_boundaries(self):
        arr = DynamicArray()
        for i in range(100):
            arr.append(i)
        self.assertEqual(arr.capacity, 128)
        for _ in range(80):
            arr.remove(0)
        self.assertEqual(arr.capacity, 64)
        self.assertEqual(list(arr), list(range(80, 100)))
        while len(arr):
            arr.remove(len(arr) - 1)
        self.assertEqual(arr.capacity, 1)
        arr.insert(0, None)
        self.assertIsNone(arr.get(0))
        for operation in (lambda: arr.insert(2, 3), lambda: arr.remove(-1),
                          lambda: arr.get(1), lambda: arr._resize(0)):
            with self.assertRaises((IndexError, ValueError)):
                operation()

    def test_gold(self):
        for factor in (0, 1, -1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                DynamicArrayGold(factor)
        for factor in ("2", None, True):
            with self.assertRaises(TypeError):
                DynamicArrayGold(factor)
        for factor in (1.01, 1.5, 2.0):
            arr = DynamicArrayGold(factor)
            for i in range(100):
                previous = arr.capacity
                was_full = len(arr) == previous
                arr.insert(len(arr), i)
                if was_full:
                    self.assertEqual(arr.capacity, int(previous * factor) + 1)
            self.assertEqual(list(arr), list(range(100)))

    def test_randomized_against_python_list(self):
        for factory in (DynamicArray, lambda: DynamicArrayGold(1.5), DynamicArrayGold):
            rng = random.Random(2026)
            arr, reference = factory(), []
            for _ in range(1500):
                operation = rng.randrange(4)
                value = rng.randrange(-10, 11)
                if operation == 0 or not reference:
                    arr.append(value)
                    reference.append(value)
                elif operation == 1:
                    index = rng.randrange(len(reference) + 1)
                    arr.insert(index, value)
                    reference.insert(index, value)
                elif operation == 2:
                    index = rng.randrange(len(reference))
                    arr.remove(index)
                    reference.pop(index)
                else:
                    index = rng.randrange(len(reference))
                    arr.set(index, value)
                    reference[index] = value
                self.assertEqual(list(arr), reference)
                self.assertGreaterEqual(arr.capacity, max(1, len(arr)))


if __name__ == "__main__":
    unittest.main()
