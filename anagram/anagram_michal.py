from collections import Counter
from math import prod, factorial


def listPosition(word):
    cur_prefix = ""
    index = 1
    for slot in word:
        established = cur_prefix
        cur_prefix += slot
        letters_left = list(word)
        for letter in established:
            letters_left.remove(letter)
        for letter in sorted(set(letters_left)):
            if letter < slot:
                prefix = established + letter
                letters_left_here = list(word)
                for c_letter in prefix:
                    letters_left_here.remove(c_letter)
                index += num_of_permutations(letters_left_here)
            else:
                break
    return index


def num_of_permutations(items):
    if not items:
        return 1
    counts = Counter(items)
    return factorial(len(items)) // prod(factorial(count) for key, count in counts.items())
