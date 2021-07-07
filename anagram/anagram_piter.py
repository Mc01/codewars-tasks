import math
from collections import Counter


def permutations_for_letter(letter, counter, number_of_letters):
    order = sorted(counter.keys())
    numerator = math.factorial(number_of_letters)
    position = 0
    for val in order:
        counter[val] -= 1
        if val == letter:
            break
        denominator = 1
        for amount in counter.values():
            denominator *= math.factorial(amount)
        position += numerator // denominator
        counter[val] += 1
    return position


def listPosition(word):
    counter = Counter(word)
    number_of_letters = len(word)
    position = 0
    for letter in word:
        number_of_letters -= 1
        position += permutations_for_letter(letter, counter, number_of_letters)
        if counter[letter] == 0:
            del counter[letter]
    return position + 1
