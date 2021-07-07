from collections import Counter
from math import factorial, prod


factor_cache = {}


def factor(v: int):
    try:
        return factor_cache[v]
    except KeyError:
        factor_cache[v] = factorial(v)
        return factor_cache[v]


def listPosition(word):
    alphabet = sorted(word)
    combinations = 0

    for position in word:
        previous = None

        for j, letter in enumerate(alphabet):
            if letter == previous:
                continue
            elif letter < position:
                available = alphabet[:j] + alphabet[j + 1:]
                duplicates = Counter(available)

                non_unique_combinations = factor(len(alphabet) - 1)
                duplicated_combinations = 1
                for key in duplicates:
                    duplicated_combinations *= factor(duplicates[key])

                combinations += non_unique_combinations // duplicated_combinations
                previous = letter
            else:
                alphabet.pop(j)
                break

    return combinations + 1


if __name__ == '__main__':
    testValues = {
        'A': 1,
        'ABAB': 2,
        'AAAB': 1,
        'BAAA': 4,
        'QUESTION': 24572,
        'BOOKKEEPER': 10743,
        'IMMUNOELECTROPHORETICALLY' * 100: 718393983731145698173,
        'DCCBBAA': 630,
        'TOFFEE': 180,
    }
    for word, value in testValues.items():
        print(listPosition(word), value)
