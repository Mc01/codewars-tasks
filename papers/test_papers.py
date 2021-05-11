import random
import string
import time
from decimal import Decimal

from papers import Inspector as MarcinInspector


# players
player_inspectors = {
    "Marcin": MarcinInspector,
}

# configuration
bulletin_multiplier = 1000
work_pass_multiplier = 3000
persons_multiplier = 1000

# init
bulletin = '\n'.join(['''Allow citizens of Obristan
Entrants require passport
Foreigners require access permit
Entrants require measles vaccination
Entrants no longer require measles vaccination'''] * bulletin_multiplier) + (
    '''\nAllow citizens of Arstotzka
    Deny citizens of Obristan
    Allow citizens of Obristan
    Entrants require measles vaccination'''
)

persons = [
    {
        'passport': 'ID#: PD8LK-9YIE8\nNATION: Obristan\nNAME: Andrevska, Gunther\nDOB: 1968.08.29\nSEX: M\nISS: Bostan\nEXP: 1984.08.05',
        'certificate_of_vaccination': f'NAME: Andrevska, Gunther\nID#: PD8LK-9YIE8\nVACCINES: {"measles, " if i % 2 == 0 else ""}tetanus, rubella, typhus, cholera',
        'access_permit': 'NAME: Andrevska, Gunther\nNATION: Obristan\nID#: PD8LK-9YIE8\nPURPOSE: WORK\nDURATION: 3 MONTHS\nHEIGHT: 152cm\nWEIGHT: 115kg\nEXP: 1992.05.08',
        'work_pass': '\n'.join([f'{random.choice(string.ascii_uppercase)}: {string.ascii_lowercase}' for _ in range(work_pass_multiplier)])
    } for i in range(persons_multiplier)
]

# debug
print(f"Generated configuration: bulletin chars: {len(bulletin)} + persons: {len(persons)}")

# execution
scores = {}
for player, inspector_class in player_inspectors.items():
    solution = []
    start = Decimal(str(time.time()))
    current_inspector = inspector_class()
    current_inspector.receive_bulletin(bulletin)
    for person in persons:
        solution.append(current_inspector.inspect(person))
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
