"""Запуск: python demo.py."""

from static_array import StaticArray
from dynamic_array import DynamicArray
from dynamic_array_gold import DynamicArrayGold


def main():
    fixed = StaticArray(3)
    for value in (10, 20, 30):
        fixed.append(value)
    fixed.set(1, 99)
    print("StaticArray:", fixed, "length:", len(fixed), "get(1):", fixed.get(1))
    try:
        fixed.append(40)
    except OverflowError as error:
        print("Expected error:", error)
    array = DynamicArray()
    for value in range(0, 20, 2):
        array.append(value)
    array.insert(3, 999)
    print("After insert:", array)
    array.remove(3)
    print("After remove:", array)
    print("find(6):", array.find(6), "binary_search(6):", array.binary_search(6))
    print("Missing:", array.find(100), array.binary_search(100))
    for factor in (2.0, 1.5):
        gold = DynamicArrayGold(factor)
        for value in range(100):
            gold.append(value)
        print("Factor:", factor, "size:", len(gold), "capacity:", gold.capacity)


if __name__ == "__main__":
    main()
