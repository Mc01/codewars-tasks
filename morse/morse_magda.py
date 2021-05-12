import itertools
from morse import MORSE_CODE


def decode_bits(bits):
    bits = bits.strip("0")
    chunks = ["".join(g) for k, g in itertools.groupby(bits)]
    chunks.sort(key=len)
    unit_length = len(chunks[0])
    return bits.replace('111'*unit_length, '-').replace('000'*unit_length, ' ')\
        .replace('1'*unit_length, '.').replace('0'*unit_length, '')


def decode_morse(morse_code):
    words = ["".join([MORSE_CODE[letter] for letter in words.split()]) for words in morse_code.split("  ")]
    return " ".join([word for word in words if word != ""])
