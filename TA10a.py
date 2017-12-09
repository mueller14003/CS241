"""
File: ta10-solution.py
Author: Br. Burton
This file demonstrates the merge sort algorithm. There
are efficiencies that could be added, but this approach is
made to demonstrate clarity.
"""
from random import randint
MAX_NUM = 100


def quick_sort(items, start, end):
    if start < end:
        pos = partition(items, start, end)
        quick_sort(items, start, pos - 1)
        quick_sort(items, pos + 1, end)

    return items


def partition(items, start, end):
    pos = start

    for i in range(start, end):
        if items[i] < items[end]:
            items[i], items[pos] = items[pos], items[i]
            pos += 1

    items[pos], items[end] = items[end], items[pos]

    return pos


def generate_list(size):
    """
    Generates a list of random numbers.
    """
    items = [randint(0, MAX_NUM) for i in range(size)]
    return items


def display_list(items):
    """
    Displays a list
    """
    for item in items:
        print(item)


def main():
    """
    Tests the merge sort
    """
    size = int(input("Enter size: "))

    items = generate_list(size)
    items = quick_sort(items, 0, len(items) - 1)

    print("\nThe Sorted list is:")
    display_list(items)


if __name__ == "__main__":
    main()
