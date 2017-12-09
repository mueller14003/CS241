"""
File: ta10-solution.py
Author: Br. Burton
This file demonstrates the merge sort algorithm. There
are efficiencies that could be added, but this approach is
made to demonstrate clarity.
"""

from random import randint
MAX_NUM = 100


def merge(left, right):
    left_i = 0
    right_i = 0
    result = []
    while left_i < len(left) and right_i < len(right):
        if left[left_i] < right[right_i]:
            result.append(left[left_i])
            left_i += 1
        else:
            result.append(right[right_i])
            right_i += 1

    result += left[left_i:]
    result += right[right_i:]
    return result


def merge_sort(items):
    """
    Sorts the items in the list
    :param items: The list to sort
    """
    if len(items) == 1:
        return items

    half = len(items)//2
    left = merge_sort(items[:half])
    right = merge_sort(items[half:])

    return merge(left, right)


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
    items = merge_sort(items)

    print("\nThe Sorted list is:")
    display_list(items)


if __name__ == "__main__":
    main()
