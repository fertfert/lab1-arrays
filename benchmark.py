"""Воспроизводимые измерения; подготовка данных вне замера поиска."""

import csv
import gc
import platform
import statistics
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from dynamic_array import DynamicArray
from dynamic_array_gold import DynamicArrayGold

OUT = Path(__file__).resolve().parent / "results"


def timed(action):
    gc.collect()
    start = time.perf_counter()
    action()
    return time.perf_counter() - start


def main():
    OUT.mkdir(exist_ok=True)
    rows = []
    for n in (1000, 5000, 10000, 50000, 100000):
        for factor in (2.0, 1.5):
            samples = []
            for repeat in range(5):
                arr = DynamicArrayGold(factor)
                def append_all():
                    for i in range(n):
                        arr.append(i)
                elapsed = timed(append_all)
                assert len(arr) == n and arr.get(n - 1) == n - 1
                samples.append(elapsed)
                rows.append(("growth", n, factor, repeat + 1, elapsed, arr.capacity))
            print(f"n={n}, factor={factor}: {statistics.median(samples):.6f} s", flush=True)
    with (OUT / "growth.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(("experiment", "n", "factor", "repeat", "seconds", "capacity"))
        writer.writerows(rows)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    for factor in (2.0, 1.5):
        sizes = sorted({row[1] for row in rows})
        times = [statistics.median(row[4] for row in rows if row[1] == n and row[2] == factor) for n in sizes]
        capacities = [next(row[5] for row in rows if row[1] == n and row[2] == factor) for n in sizes]
        axes[0].plot(sizes, times, "o-", label=f"factor = {factor}")
        axes[1].plot(sizes, capacities, "o-", label=f"factor = {factor}")
    for ax, ylabel in zip(axes, ("Время n добавлений, с", "Ёмкость, ячеек")):
        ax.set(xlabel="Количество элементов n", ylabel=ylabel)
        ax.grid(alpha=0.3)
        ax.legend()
    fig.suptitle("ЛР1: коэффициенты роста (медиана 5 запусков)")
    fig.tight_layout()
    fig.savefig(OUT / "growth.png", dpi=160)
    plt.close(fig)

    searches = []
    for n in (1000, 5000, 10000, 50000, 100000):
        arr = DynamicArray()
        for i in range(n):
            arr.append(i)
        for name, method in (("linear", arr.find), ("binary", arr.binary_search)):
            for repeat in range(5):
                def search_many():
                    for _ in range(100):
                        method(n - 1)
                assert method(n - 1) == n - 1
                searches.append((n, name, repeat + 1, timed(search_many) / 100))
    with (OUT / "search.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(("n", "method", "repeat", "seconds_per_search"))
        writer.writerows(searches)
    fig, ax = plt.subplots(figsize=(8, 5))
    for name in ("linear", "binary"):
        sizes = sorted({row[0] for row in searches})
        ax.plot(sizes, [statistics.median(row[3] for row in searches if row[0] == n and row[1] == name) for n in sizes], "o-", label=name)
    ax.set(xlabel="Количество элементов n", ylabel="Время одного поиска, с (лог. шкала)",
           title="Поиск последнего элемента: медиана 5 серий по 100 запросов", yscale="log")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "search.png", dpi=160)
    plt.close(fig)
    (OUT / "environment.txt").write_text(
        f"Python {platform.python_version()}\n{platform.platform()}\n"
        "Clock: time.perf_counter\nRepeats: 5\nSearches per repeat: 100\n"
        "GC: collected before each timed batch, enabled during batch\n", encoding="utf-8")


if __name__ == "__main__":
    main()
