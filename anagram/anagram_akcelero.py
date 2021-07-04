from collections import defaultdict


def listPosition(word):
    possible_letters = defaultdict(lambda: 0)  # empty dict on the very beginning
    result = 0
    dividend = 1  # will factorial of next numbers
    divider = 1 # will be constructed in each

    for i, first_letter in enumerate(word[::-1], start=1):

        possible_letters[first_letter] += 1

        divider *= possible_letters[first_letter]

        possible_on_first_place = sum(number for letter, number in possible_letters.items() if letter < first_letter)

        result += possible_on_first_place * dividend // divider

        dividend *= i

    return result + 1 # result should be counted from 1
