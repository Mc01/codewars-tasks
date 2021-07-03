from collections import Counter
from math import factorial, prod


def listPosition(word):
    alphabet = sorted(word)
    combinations = 0

    for position in word:
        previous = None

        for j, letter in enumerate(alphabet):
            if alphabet[j] == previous:
                continue
            elif letter < position:
                available = alphabet[:j] + alphabet[j + 1:]
                duplicates = Counter(available)

                non_unique_combinations = factorial(len(available))
                duplicated_combinations = prod(
                    factorial(v) for v in duplicates.values()
                )
                unique_combinations = non_unique_combinations // duplicated_combinations

                combinations += unique_combinations
                previous = alphabet[j]
            else:
                alphabet.pop(j)
                break

    return combinations + 1


testValues = {
    'A': 1,
    'ABAB': 2,
    'AAAB': 1,
    'BAAA': 4,
    'QUESTION': 24572,
    'BOOKKEEPER': 10743,
    'IMMUNOELECTROPHORETICALLY': 718393983731145698173,
    'DCCBBAA': 629,
    'TOFFEE': 180,
}
for word, value in testValues.items():
    print(listPosition(word), value)
