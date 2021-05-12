from operator import gt, lt
from copy import copy
from typing import List, Dict
import enum


class Dinglemouse(object):
    lift = None

    def __init__(self, queues, capacity):
        self.lift = Lift(queues, capacity)

    def theLift(self):
        return self.lift.run()


class Direction(enum.IntEnum):
    UP = 1
    DOWN = -1

    def reverse(self):
        return Direction(self.value * -1)

    @property
    def operator(self):
        return {
            Direction.UP: gt,
            Direction.DOWN: lt,
        }[self]

    @property
    def get_nearest(self):
        return {
            Direction.UP: min,
            Direction.DOWN: max,
        }[self]


class LiftFull(Exception):
    pass


class InvalidMove(Exception):
    pass


class InvalidFloor(Exception):
    pass


class Lift:
    commands: List[Dict[Direction, List[int]]]
    capacity: int = 0
    visited_floors: List[int] = None
    current_floor: int = 0
    passengers: List[int] = None
    direction: Direction = None

    def __init__(self, queues, capacity):
        self.commands = [
            {
                Direction.UP: [p for p in queue if p > floor],
                Direction.DOWN: [p for p in queue if p < floor]
            } for floor, queue in enumerate(queues)
        ]
        self.capacity = capacity
        self.current_floor = 0
        self.visited_floors = []
        self.passengers = list()
        self.direction = Direction.UP

    @property
    def finished(self):
        if len(self.passengers) > 0:
            return False
        for commands in self.commands:
            if any(commands.values()):
                return False
        return True

    @property
    def is_full(self):
        return len(self.passengers) == self.capacity

    @property
    def is_empty(self):
        return len(self.passengers) == 0

    def run(self):
        while True:
            if not self.visited_floors:
                self.visited_floors.append(self.current_floor)
            elif self.visited_floors[-1] != self.current_floor:
                self.visited_floors.append(self.current_floor)
            if self.finished:
                break
            passengers_on_arrival = copy(self.passengers)
            try:
                self.let_passengers_out(self.current_floor)
            except InvalidFloor:
                print(f"noone leaving at {self.current_floor}")
            try:
                self.get_passengers_in(self.current_floor)
            except InvalidFloor:
                print(f"noone to pick up at {self.current_floor}")
            except LiftFull:
                print(f"lift full, can not pick up from {self.current_floor}")

            try:
                self.move()
            except InvalidMove:
                self.change_direction()
                print(f"no next stop, changing direction, going {self.direction.name}")
                continue
        try:
            if self.visited_floors[-1] != 0:
                self.visited_floors.append(0)
            return self.visited_floors
        except IndexError:
            return [0]

    def move(self):
        next_stop = self.next_stop()
        if next_stop is None:
            raise InvalidMove("No next stop")
        self.current_floor = next_stop

    def next_stop(self):
        opr = self.direction.operator
        get_nearest = self.direction.get_nearest

        if self.direction is Direction.UP:
            possible_passengers = [
                i
                for i, commands in enumerate(self.commands[self.current_floor + 1:], start=self.current_floor + 1)
                if commands[self.direction]
            ]
        else:
            possible_passengers = [
                i
                for i, commands in enumerate(self.commands[:self.current_floor])
                if commands[self.direction]
            ]
        possible_passengers = possible_passengers or []
        possible_passengers.extend(self.passengers)
        if possible_passengers:
            if len(possible_passengers) > 1:
                return get_nearest(*possible_passengers)
            else:
                return possible_passengers[0]
        if self.is_empty:
            if self.direction is Direction.UP:
                for i, commands in enumerate(self.commands[self.current_floor + 1:][::-1], start=1):
                    if commands[self.direction.reverse()]:
                        self.change_direction()
                        return len(self.commands) - i
            else:
                for i, commands in enumerate(self.commands[:self.current_floor]):
                    if commands[self.direction.reverse()]:
                        self.change_direction()
                        return i
        if self.finished:
            return 0
        else:
            return None

    def let_passengers_out(self, floor: int):
        if floor not in self.passengers:
            raise InvalidFloor("no one leaving")
        self.passengers = [p for p in self.passengers if p != floor]

    def get_passengers_in(self, floor: int):
        opr = self.direction.operator
        waiting = self.commands[floor][self.direction]
        if not waiting:
            raise InvalidFloor("no one to pick up")
        capacity = self.capacity - len(self.passengers)
        if capacity == 0:
            raise LiftFull()
        new_passengers = self.commands[floor][self.direction][:capacity]
        self.commands[floor][self.direction] = self.commands[floor][self.direction][capacity:]
        self.passengers.extend(new_passengers)

    def change_direction(self):
        self.direction = self.direction.reverse()
