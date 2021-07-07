import copy
import math


def listPosition(word):
    return Anagram(word).get_anagram_position()


class Anagram:
    word = ""
    word_len = 0
    ordered_letters = []
    ordered_letters_freq = {}
    _sum_anagrams = 1
    _current_nominator = 0

    def __init__(self, word):
        self.word = word
        self.word_len = len(self.word)
        self.ordered_letters = sorted(set(self.word))
        ordered_letters_freq = dict.fromkeys(self.ordered_letters, 0)
        for letter in self.word:
            ordered_letters_freq[letter] += 1
        self.ordered_letters_freq = ordered_letters_freq

    def _count_num_anagrams(self, prefix):
        ordered_letters_freq = copy.deepcopy(self.ordered_letters_freq)
        for letter in prefix:
            if ordered_letters_freq[letter] > 0:
                ordered_letters_freq[letter] -= 1
            else:
                return
        self._sum_anagrams += self._current_nominator // math.prod(
            [math.factorial(value) for value in list(ordered_letters_freq.values())]
        )

    def _process_letter(self, letter, prefix):
        for l in self.ordered_letters:
            new_prefix = f"{prefix}{l}"
            if letter == l:
                return new_prefix
            else:
                self._count_num_anagrams(new_prefix)

    def get_anagram_position(self):
        prefix = ""
        for length, letter in enumerate(self.word, start=1):
            self._current_nominator = math.factorial(self.word_len - length)
            prefix = self._process_letter(letter, prefix)
        return self._sum_anagrams
