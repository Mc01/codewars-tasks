class SumTree:
    def __init__(self, word):
        letters = sorted(set(word))
        self.first_leaf = 1
        while self.first_leaf <= len(letters):
            self.first_leaf *= 2
        self.arr = [0 for _ in range(self.first_leaf * 2)]
        self.letters = {l: self.first_leaf + i + 1 for i, l in enumerate(letters)}

    def increment_and_get(self, letter):
        result = 0
        node = self.letters[letter]
        letter_num = self.arr[node] + 1
        self.arr[node] = letter_num
        while node ^ 1:
            if node & 1:
                result += self.arr[node - 1]
            node >>= 1
            self.arr[node] += 1
        return letter_num, result


def listPosition(word):
    sum_tree = SumTree(word)
    result = 0
    dividend = 1  # will factorial of next numbers
    divider = 1 # will be constructed in each
    for i, first_letter in enumerate(word[::-1], start=1):
        letter_num, possible_on_first_place = sum_tree.increment_and_get(first_letter)
        divider *= letter_num
        result += possible_on_first_place * dividend // divider
        dividend *= i
    return result + 1 # result should be counted from 1
