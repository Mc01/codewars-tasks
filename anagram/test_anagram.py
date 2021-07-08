import time
from decimal import Decimal
from random import randint, choice
from string import ascii_letters, digits

from anagram import listPosition as MarcinAnagram
from anagram_akcelero import listPosition as AkceleroAnagram
from anagram_ania import listPosition as AniaAnagram
from anagram_magda import listPosition as MagdaAnagram
from anagram_michal import listPosition as MichalAnagram
from anagram_piter import listPosition as PiterAnagram
from anagram_radek import listPosition as RadekAnagram


# players
players = {
    "Marcin": MarcinAnagram,      # A8, MA6, MI7, P7, R7, J7, M5 ->
    "Akcelero": AkceleroAnagram,  # A4, MA5, MI5, P7, R8, J9, M6 -> 44 / 7
    "Ania": AniaAnagram,          # A5, MA4, MI4, P4, R6, J6, M5 ->
    # "Janek": JanekAnagram,
    "Magda": MagdaAnagram,        # A7, MA5, MI8, P9, R8, J9, M8 ->
    "Michal": MichalAnagram,      # A6, MA5, MI5, P5, R5, J7, M5 ->
    "Piter": PiterAnagram,        # A8, MA7, MI7, P5, R7, J8, M7 ->
    "Radek": RadekAnagram,        # A7, MA8, MI7, P9, R5, J9, M9 ->
}

# 1000 + 5% od 2 do 12
# Akcelero: 0.019937 seconds
# Magda: 0.1692328 seconds
# Radek: 0.180838 seconds
# Piter: 0.9216808 seconds
# Marcin: 2.392875 seconds
# Michal: 5.484945 seconds
# Ania: 6.4498662 seconds

# configuration
alphabet = ascii_letters + digits
length = 250
repetitions_occurrence_percent = 30
min_repetitions = 2
max_repetitions = 10
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

# print(words)
# words = ['xyyX8cPy7QQYR111111111tXAJdJJJJJJJsy2b55H7ShTCYQiPXuYWN66Cx4pi39J8VxUMMC9Svs2WBMEUlLWwwwwwwwwwwwj4zBIT6Y4F1qfLxbFIN5D6D8888888888AgMhMDohtFKVXyGVaWbHUiaZst9JvuC1Z90S3PPPPPzpDay168TgJJJJJJJJJJJJ3ac0A6r8888888888882xzoKvzzW2EaCgXQJKtbu6HGkvMX4NELYPPPPPPPPPPPGtYDkojI4IAROruCbxIIIIvvvvMeAOXllllll8YL4RJfQ0eExU03b2FxgrVyIjozIrPvagm6sm9JJjQKQUZVzC1KKK09UHHHHaX3P4MMMMeitlEfWlmN33eswZXPLOBzMBfAYWWWWWWIEfP632IbpgeAKKBuQJWJ7jpKKKKnukS0xBQTX8IR7oGi91ppfMazYXlmvhJoFQllllpZ43zrZ1hNkkkk9YZZZZZZZZZZZZuNOLZkV6O1uHNkvOA10nicVnEEEEEpZtjhuE6CFqvszVpUVcYC1eyX7HXccpldT12VzEIhcsevUnyaaaaaaaaaaaB16pJQ57W3ITfhDTyiHaj7ooooooog9AES4TI5CPLn4OL3H9zJMd3AHZPEwogFGnZYSRzwsry3UditSlssNTmHQXr6aN0CARFFFFF9w7l1lqqqqqqqqqqqqTppppE2UoSbuqeAqGGGGYYYN0vR6NossssssssssgaJXWhVR2egXb5zeq5xNNNNNNNNNvQOZBIeebeWb4U3GrXjqx2By2RHeITB8ttttKjRYgNPnQOFTxJvGH3mUPP5KKqkfv4gLSXtpUprjjjjjjjjjD8JuHGFxOC3SsJmIx2LLLLLzkHQVQwfpLRCi9UWLS4NqSOVsjxYFCBfzACd55DRoVPkI9GOklOaojpqZ2M66666666666OOTDxxg7D8zzzzzzzzzPhaLHOx21oxrF4133UAstJag5DABLoBnKt92lll']

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
    # for i, word in enumerate(words):
    #     print(f"{player} word {i}: {place[word]['time']:.5f} seconds")

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
        print(f"Solution: {list(grouped_answers.keys())[i]}")
