class Direction:
    UP = 0
    DOWN = 1


class Dinglemouse(object):
    def __init__(self, queues, capacity):
        self.going_up = {lvl: [p for p in queue if p > lvl] for lvl, queue in enumerate(queues) if queue}
        self.going_up = {k: v for k,v in self.going_up.items() if v}
        self.going_down = {lvl: [p for p in queue if p < lvl] for lvl, queue in enumerate(queues) if queue}
        self.going_down = {k: v for k,v in self.going_down.items() if v}
        self.current_level = 0
        self.direction = Direction.UP
        self.passengers = []
        self.result = [0]
        self.max_level = len(queues) - 1
        self.capacity = capacity

    @property
    def potential_passengers(self):
        return self.going_up if self.direction == Direction.UP else self.going_down
    def check_if_need_to_stop(self):
        if self.result[-1] == self.current_level:
            return
        if self.potential_passengers.get(self.current_level) or any(
                True for p in self.passengers if p == self.current_level):
            self.result.append(self.current_level)

    def move_to_next_floor(self):
        if self.direction == Direction.UP:
            if self.current_level == self.max_level:
                self.direction = Direction.DOWN
            else:
                potential_next_stop = [p for p in self.going_up.keys() if p > self.current_level]
                potential_next_stop += self.passengers
                self.current_level = min(potential_next_stop, default=self.max_level)
        else:
            if self.current_level == 0:
                self.direction = Direction.UP
            else:
                potential_next_stop = [p for p in self.going_down.keys() if p < self.current_level]
                potential_next_stop += self.passengers
                self.current_level = max(potential_next_stop, default=0)

    def drop_passengers(self):
        self.passengers = [p for p in self.passengers if p != self.current_level]

    def take_passengers(self):
        to_be_taken = min(self.capacity - len(self.passengers),
                          len(self.potential_passengers.get(self.current_level, [])))
        if to_be_taken:
            self.passengers += self.potential_passengers[self.current_level][:to_be_taken]
            self.potential_passengers[self.current_level] = self.potential_passengers[self.current_level][to_be_taken:]
            if not self.potential_passengers[self.current_level]:
                self.potential_passengers.pop(self.current_level)

    def theLift(self):
        while self.going_up or self.going_down or self.passengers:
            self.check_if_need_to_stop()
            self.drop_passengers()
            self.take_passengers()
            self.move_to_next_floor()
        if self.result[-1] != 0:
            self.result.append(0)
        return self.result
