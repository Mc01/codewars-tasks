from enum import Enum, auto
from functools import reduce


class Direction(Enum):
    UP = auto()
    DOWN = auto()


class Dinglemouse(object):

    def __init__(self, queues, capacity):
        self.going_up = {lvl: [p for p in queue if p > lvl] for lvl, queue in enumerate(queues) if queue}
        self.going_down = {lvl: [p for p in queue if p < lvl] for lvl, queue in enumerate(queues) if queue}
        self.current_level = 0
        self.direction = Direction.UP
        self.passengers = []
        self.result = [0]
        self.max_level = len(queues) - 1
        self.capacity = capacity

    @property
    def potential_passengers(self):
        return self.going_up if self.direction == Direction.UP else self.going_down

    def drop_passengers(self):
        self.passengers = [p for p in self.passengers if p != self.current_level]

    def check_if_need_to_stop(self):
        if self.potential_passengers.get(self.current_level) or any(
                True for p in self.passengers if p == self.current_level):
            self.result.append(self.current_level)

    def move_to_next_floor(self):
        if self.direction == Direction.UP:
            if self.current_level == self.max_level:
                self.direction = Direction.DOWN
            else:
                self.current_level += 1
        else:
            if self.current_level == 0:
                self.direction = Direction.UP
            else:
                self.current_level -= 1

    def take_passengers(self):
        to_be_taken = min(self.capacity - len(self.passengers),
                          len(self.potential_passengers.get(self.current_level, [])))
        if to_be_taken:
            self.passengers += self.potential_passengers[self.current_level][:to_be_taken]
            self.potential_passengers[self.current_level] = self.potential_passengers[self.current_level][to_be_taken:]

    def remove_stops_same_in_row(self):
        self.result = list(
            reduce((lambda prev, e: prev + ([e] if e != prev[-1] else [])), self.result[1:], self.result[:1]))

    def theLift(self):
        while any(self.going_up.values()) or any(self.going_down.values()) or self.passengers:
            self.check_if_need_to_stop()
            self.drop_passengers()
            self.take_passengers()
            self.move_to_next_floor()

        self.result.append(0)
        self.remove_stops_same_in_row()

        return self.result
