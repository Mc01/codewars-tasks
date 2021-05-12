import re
from morse import MORSE_CODE


def decode_bits(bits):
    bits_stripped = bits.strip('0')
    if not '0' in bits_stripped:
        return '.'
    transmission_rate = len(min(re.findall('(1+|0+)', bits_stripped), key=len))
    return bits_stripped[::transmission_rate].replace('111', '-').replace('000', ' ').replace('1', '.').replace('0', '')


def decode_morse(morse_code):
    result = ""
    for word in morse_code.split('  '):
        result += f" {''.join([MORSE_CODE[letter] for letter in word.split(' ')])}"
    return result.strip(' ')