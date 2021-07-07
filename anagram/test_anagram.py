import time
from decimal import Decimal
from random import randint, choice
from string import ascii_letters, digits

from anagram import listPosition as MarcinAnagram
from anagram_magda import listPosition as MagdaAnagram


# players
players = {
    "Marcin": MarcinAnagram,
    # "Akcelero": AkceleroAnagram,
    # "Ania": AniaAnagram,
    # "Janek": JanekAnagram,
    "Magda": MagdaAnagram,
    # "Michal": MichalAnagram,
    # "Piter": PiterAnagram,
    # "Radek": RadekAnagram,
}

# configuration
alphabet = ascii_letters + digits
length = 1000
repetitions_occurrence_percent = 15
min_repetitions = 3
max_repetitions = 15
word_count = 1
words = []

# init
for _ in range(word_count):
    word = ''
    while len(word) < length:
        letter = choice(alphabet)

        repetition_chance = randint(0, 100)
        if repetition_chance < repetitions_occurrence_percent:
            repetitions = randint(min_repetitions, max_repetitions)
            letter *= repetitions

        word += letter
        if len(word) > length:
            word = word[:length]

    words.append(word)

# execution
scores = {}
for player, anagram in players.items():
    average = 0
    for word in words:
        start = Decimal(str(time.time()))
        solution = anagram(word)
        stop = Decimal(str(time.time()))
        duration = stop - start
        average += duration
        scores.setdefault(player, {})[word] = {
            "time": duration,
            "solution": solution,
        }

    average /= len(words)
    scores[player]["average"] = average


# performance check
sorted_times = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1]["average"])}
for player, place in sorted_times.items():
    print(f"{player}: {place['average']} seconds")
    for i, word in enumerate(words):
        print(f"{player} word {i}: {place[word]['time']:.5f} seconds")

    print("---***---***---***---***---***---")

# group by solution
grouped_answers = {}
for player, answer in scores.items():
    for word in words:
        solution = answer[word]["solution"]
        grouped_answers.setdefault(solution, []).append(player)

# solution check
if len(grouped_answers.keys()) == len(words):
    print("All players have same solution")
else:
    for i, owners in enumerate(grouped_answers.values()):
        print(f"Players with similar solutions - group {i + 1}: {owners}")
        # print(f"Solution: {list(grouped_answers.keys())[i]}")
