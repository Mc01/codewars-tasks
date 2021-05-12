from morse import MORSE_CODE


def decode_bits(bits):
    assert all(b in ["1", "0"] for b in bits) == True # check if bits consists only of 1's and 0's
    bits = bits.strip("0") # assure there is no trailing and initial 0's
    # find how long is time unit
    s = 0 # shortest time unit
    bit = bits[0]
    counter = 1
    for b in bits[1:]:
        if bit == b:
            counter += 1
        else:
            if not s or counter <= s:
                s = counter
            counter = 1
            bit = b
    # if bits consists only with 1's then s is length of bits
    if s == 0:
        s = len(bits)
    # replace bits with dashes, dots and spaces
    return bits.replace(s * '111', '-').replace(s * '000', ' ').replace(s * '1', '.').replace(s * '0', '')


def decode_morse(morseCode):
    assert all(m in [" ", ".", "-"] for m in morseCode) == True # check if code consist only of ".", "-" and spaces
    return " ".join(["".join(MORSE_CODE[l] for l in w) for w in [m_w.split() for m_w in morseCode.split(2 * " ")]])
