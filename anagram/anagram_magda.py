import math
from collections import Counter


def listPosition(word):
    rank = 1

    alphabetic_order = sorted(set(word))
    letters_order = [alphabetic_order.index(letter) for letter in word]
    word_len = len(word)

    for idx, order in enumerate(letters_order):

        divider = 1
        repetitions = Counter(word[idx:])
        for letter in repetitions.keys():
            divider *= math.factorial(repetitions[letter])

        smaller = 0
        for o in letters_order[idx + 1:]:
            if order > o:
                smaller += 1

        rank += (smaller * math.factorial(word_len - idx - 1)) // divider

    return rank
