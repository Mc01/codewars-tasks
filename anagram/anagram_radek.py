import math

from collections import Counter
from functools import reduce

import sys
import threading

sys.setrecursionlimit(10**5)  # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size


def num_permutations(word):
    letter_frequencies = Counter(word)
    f = math.factorial(len(word))
    div = 1
    for frequency in letter_frequencies.values():
        div *= math.factorial(frequency)
    return f // div


def listPosition(word):
    if len(word) == 1:
        return 1
    else:
        sorted_letters = sorted(word)
        first_order = sorted_letters.index(word[0])
        tail_position = listPosition(word[1:])
        return first_order * num_permutations(word) // len(word) + tail_position


def listPositionNoRecur(word):
    def inner(acc, letter):
        index = sorted_letters.index(letter)
        sorted_letters.remove(letter)
        letters_ahead = list(dict.fromkeys(sorted_letters[:index]))

        return acc + reduce(
            lambda a, l: a + num_permutations("".join(sorted_letters).replace(l, letter, 1)),
            letters_ahead,
            0,
        )

    sorted_letters = sorted(word)
    return reduce(inner, list(word), 1)
