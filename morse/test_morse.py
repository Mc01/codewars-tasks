from random import randint
import random
import time
from decimal import Decimal


# Dictionary representing the morse code chart
MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ',': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-'}


def encrypt(message):
    cipher = ''
    for letter in message:
        if letter != ' ':
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            cipher += ' '
    return cipher


def encode_binary_morse(m):
    choices = list(MORSE_CODE_DICT.keys())
    choices.append(" ")
    phrase = ''.join([''.join(random.choice(choices) for i in range(randint(100, 200)))])
    phrase = phrase.strip()
    phrase = " ".join([p.strip() for p in phrase.split() if p])
    sp_phrase = phrase.split()
    decoded_words = []
    for word in sp_phrase:
        decoded_words.append(encrypt(word))
    binary_words = []
    for word in decoded_words:
        letters = word.split()
        binary_letters = []
        for letter in letters:
            binary_chars = []
            for char in letter:
                if char == ".":
                    binary_chars.append(m * "1")
                else:
                    binary_chars.append(m * 3 * "1")
            joiner = m * "0"
            binary_letters.append(joiner.join(binary_chars))
        joiner = m * 3 * "0"
        binary_words.append(joiner.join(binary_letters))
    joiner = m * 7 * "0"
    binary_phrase = joiner.join(binary_words)
    return phrase, binary_phrase


def generate_test_set():
    test_set = []  # results like [(phrase, binary_code), (phrase, binary_code)...]
    for i in range(3000):
        test_set.append(encode_binary_morse(randint(1, 10)))
    return test_set


def perform_test(test_set, player, fun_1, fun_2):
    wrong = 0
    start = Decimal(str(time.time()))
    for t in test_set:
        if t[1]:
            res = fun_1(fun_2(t[1]))
            if res != t[0]:
                wrong += 1
    stop = Decimal(str(time.time()))
    test_results[player]["time"] = stop - start
    test_results[player]["wrong"] = wrong


test_set = generate_test_set()
test_results = {
    "Marcin": {"time": 0, "wrong": 0},
    "Janek": {"time": 0, "wrong": 0},
    "Magda": {"time": 0, "wrong": 0},
    "Ania": {"time": 0, "wrong": 0},
    "Radek": {"time": 0, "wrong": 0},
    "Piter": {"time": 0, "wrong": 0},
    "Michal": {"time": 0, "wrong": 0},
    "Akcelero": {"time": 0, "wrong": 0},
}

# from Marcin import decode_morse as morse
# from Marcin import decode_bits as bits
# perform_test(test_set, "Marcin", morse, bits)

from morse_janek import decode_morse as morse, decode_bits as bits
perform_test(test_set, "Janek", morse, bits)

from morse_magda import decode_morse as morse, decode_bits as bits
perform_test(test_set, "Magda", morse, bits)

from morse_ania import decode_morse as morse, decode_bits as bits
perform_test(test_set, "Ania", morse, bits)

from morse_akcelero import decode_morse as morse, decode_bits as bits
perform_test(test_set, "Akcelero", morse, bits)

from morse_piter import decode_morse as morse, decode_bits as bits
perform_test(test_set, "Piter", morse, bits)

from morse_michal import decode_morse as morse, decode_bits as bits
perform_test(test_set, "Michal", morse, bits)

# performance check
sorted_times = {k: v for k, v in sorted(test_results.items(), key=lambda item: item[1]["time"])}
for player, place in sorted_times.items():
    print(f"{player}: {place['time']} seconds")
