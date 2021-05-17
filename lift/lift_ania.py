from typing import List


class Dinglemouse:
    going_up: bool = True
    passengers: List = []
    people_waiting: bool = False

    def __init__(self, queues, capacity):
        self.queues = [list(q) for q in queues]
        self.capacity = capacity
        self.max_floor = len(queues) - 1
        self.stops = [0]

    def theLift(self):
        current_floor = 0
        while self.passengers or any(len(q) > 0 for q in self.queues):
            self.people_waiting = False
            if current_floor in self.passengers:
                self._leave_passengers(current_floor)
            for idx, request in enumerate(self.queues[current_floor]):
                if self.going_up:
                    is_person_going_same_direction = request - current_floor > 0
                else:
                    is_person_going_same_direction = request - current_floor < 0
                if (
                    is_person_going_same_direction
                    and len(self.passengers) < self.capacity
                ):
                    self._take_onboard(request, idx, current_floor)
            if self._is_last_floor(current_floor):
                self._change_direction()
                continue
            current_floor = self._move_to_next_floor(current_floor)
        self.stops.append(0)
        return self.stops

    def _is_last_floor(self, current_floor):
        return (current_floor == 0 and not self.going_up) or (current_floor == self.max_floor and self.going_up)

    def _change_direction(self):
        if self.going_up:
            self.going_up = False
        else:
            self.going_up = True

    def _leave_passengers(self, current_floor):
        self._stop_lift(current_floor)
        self.passengers = list(filter(lambda f: f != current_floor, self.passengers))

    def _stop_lift(self, current_floor):
        if self.stops[-1] != current_floor:
            self.stops.append(current_floor)

    def _take_onboard(self, request, idx_request, current_floor):
        self._stop_lift(current_floor)
        self.passengers.append(request)
        del self.queues[current_floor][idx_request]

    def _move_to_next_floor(self, current_floor):
        if self.going_up:
            return current_floor + 1
        else:
            return current_floor - 1
