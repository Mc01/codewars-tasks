from morse import MORSE_CODE


def decode_bits(bits):
    # ToDo: Accept 0's and 1's, return dots, dashes and spaces
    seq_rate = shortest_sequence(bits)
    dash = "111" * seq_rate
    word_space = "000" * seq_rate
    letter_space = "0" * seq_rate
    dot = "1" * seq_rate
    # print(bits)
    result = bits.strip("0").replace(dash, '-').replace(word_space, ' ').replace(letter_space, "").replace(dot, '.')
    # print("result:")
    # print(result)
    return result


def decode_morse(morse_code):
    # ToDo: Accept dots, dashes and spaces, return human-readable message
    words = morse_code.split("  ")
    translated_words = []
    for word in words:
        if not word:
            continue
        letters = word.split(" ")
        translated_letters = ""
        for letter in letters:
            if letter:
                translated_letters += MORSE_CODE[letter]
        translated_words.append(translated_letters)
    result = " ".join(translated_words)
    # print(result)
    return result


def shortest_sequence(_str):
    min_seq_len=len(_str)
    seq_len = 0
    for i in range(len(_str)-1):
        seq_len += 1
        if _str[i] != _str[i+1]:
            min_seq_len = min(min_seq_len, seq_len)
            seq_len = 0
    return min_seq_len
