from morse import MORSE_CODE


def decode_bits(bits):
    bits = bits.strip("0")
    lenghts_of_grouped = (len(t) for t in bits.split("0") + bits.split("1") if t)
    time_unit = min(lenghts_of_grouped, default=1)
    return (
        bits
        .replace('1' * time_unit, '1')
        .replace('0' * time_unit, '0')
        .replace('111', '-')
        .replace('1', '.')
        .replace('0' * 7, ' ; ')
        .replace('0' * 3, ' ')
        .replace('0', '')
    )


def decode_morse(morseCode):
    return ''.join(MORSE_CODE.get(c, ' ') for c in morseCode.split())
