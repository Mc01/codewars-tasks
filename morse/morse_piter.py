from morse import MORSE_CODE


def decode_bits(bits):
    # ToDo: Accept 0's and 1's, return dots, dashes and spaces
    bits = bits.lstrip('0').rstrip('0')
    ones = list(filter (None, set(bits.split('0'))))
    zeros = list(filter (None, set(bits.split('1'))))
    if len(ones) == 2:
        len_ref = len(ones[0]) if len(ones[0]) < len(ones[1]) else len(ones[1])
    else:
        len_ref = len(ones[0])
    for zero in zeros:
        len_ref = len(zero) if len(zero) < len_ref else len_ref
    return bits.replace(len_ref * '111', '-').replace(len_ref * '000', ' ').replace(len_ref * '1', '.').replace(len_ref * '0', '')


def decode_morse(morseCode):
    morseCode = morseCode.split(' ')
    result = ''
    for x in morseCode:
        result += MORSE_CODE[x] if x else ' '
    return result
