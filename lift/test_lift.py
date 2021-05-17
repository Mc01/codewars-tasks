import time
from decimal import Decimal
from random import randint

from lift import Dinglemouse as MarcinLift
from lift_janek import Dinglemouse as JanekLift
from lift_magda import Dinglemouse as MagdaLift
from lift_piter import Dinglemouse as PiterLift
from lift_radek import Dinglemouse as RadekLift
from lift_akcelero import Dinglemouse as AkceleroLift


# players
player_lifts = {
    "Marcin": MarcinLift,
    "Janek": JanekLift,
    "Magda": MagdaLift,
    # "Piter": PiterLift,
    "Radek": RadekLift,
    "Akcelero": AkceleroLift,
}

# configuration
floors = 500
min_people_on_floor = 0
max_people_on_floor = 15
capacity = 4

# init
queues = []
for i in range(floors + 1):
    floor = []

    number_of_people = randint(min_people_on_floor, max_people_on_floor)
    for person in range(number_of_people):
        random_number = randint(0, floors)
        if random_number != i:
            floor.append(random_number)

    queues.append(tuple(floor))

# debug
print(f"Generated configuration {queues}")


# execution
scores = {}
for player, lift_class in player_lifts.items():
    start = Decimal(str(time.time()))
    current_lift = lift_class(queues=tuple(queues), capacity=capacity)
    solution = current_lift.theLift()
    stop = Decimal(str(time.time()))
    scores[player] = {
        "time": stop - start,
        "solution": tuple(solution),
    }

# performance check
sorted_times = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1]["time"])}
for player, place in sorted_times.items():
    print(f"{player}: {place['time']} seconds")

# group by solution
grouped_answers = {}
for player, answer in scores.items():
    solution = answer["solution"]
    grouped_answers.setdefault(solution, []).append(player)

# solution check
if len(grouped_answers.keys()) == 1:
    print("All players have same solution")
else:
    for i, owners in enumerate(grouped_answers.values()):
        print(f"Players with solution number {i + 1}: {owners}")
