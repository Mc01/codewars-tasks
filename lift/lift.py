from typing import Optional


class Direction:
    UP = 'UP'
    DOWN = 'DOWN'


class Dinglemouse(object):
    def __init__(self, queues: tuple, capacity: int):
        self.down, self.up = {}, {}
        for floor, people in enumerate(queues):
            for person in people:
                if person < floor:
                    self.down.setdefault(floor, []).append(person)
                else:
                    self.up.setdefault(floor, []).append(person)

        self.capacity = capacity
        self.floor_history = []
        self.people_in_lift = []
        self.direction = Direction.UP
        self.visit_floor(floor=0)

    def theLift(self) -> list:
        while any((*self.up.values(), *self.down.values(), *self.people_in_lift)):
            next_floor: Optional[int] = self.next_floor()

            if next_floor is not None:
                self.visit_floor(next_floor)
            else:
                break

        if self.last_floor != 0:
            self.floor_history.append(0)

        return self.floor_history

    @property
    def last_floor(self) -> int:
        return self.floor_history[-1]

    def next_floor(self) -> Optional[int]:
        floor = self.next_floor_in_direction()
        if floor is not None:
            return floor

        self.switch_direction()
        self.take_people_new_direction()

        floor = self.next_floor_in_direction()
        return floor

    def next_floor_in_direction(self) -> Optional[int]:
        current_floor = self.floor_history[-1]

        try:
            if self.direction == Direction.UP:
                above_queue_up = [k for k in self.up.keys() if k > current_floor]
                above_queue_down = [k for k in self.down.keys() if k > current_floor]

                if not (len(self.up) or len(self.down)):
                    floor = min(self.people_in_lift)
                elif len(above_queue_up):
                    floor = min((*above_queue_up, *self.people_in_lift))
                elif len(self.people_in_lift):
                    floor = min(self.people_in_lift)
                elif len(above_queue_down):
                    floor = max(above_queue_down)
                else:
                    raise ValueError

                if floor <= current_floor:
                    raise ValueError
            else:
                below_queue_down = [k for k in self.down.keys() if k < current_floor]
                below_queue_up = [k for k in self.up.keys() if k < current_floor]

                if not (len(self.up) or len(self.down)):
                    floor = max(self.people_in_lift)
                elif len(below_queue_down):
                    floor = max((*below_queue_down, *self.people_in_lift))
                elif len(self.people_in_lift):
                    floor = max(self.people_in_lift)
                elif len(below_queue_up):
                    floor = min(below_queue_up)
                else:
                    raise ValueError

                if floor >= current_floor:
                    raise ValueError
        except ValueError:
            return None
        else:
            return floor

    def switch_direction(self):
        self.direction = (
            Direction.UP
            if self.direction == Direction.DOWN
            else Direction.DOWN
        )

    def take_people_new_direction(self):
        current_capacity = self.current_capacity
        if not current_capacity:
            return

        current_floor = self.last_floor
        if self.direction == Direction.UP and self.up.get(current_floor):
            self.take_people_up(
                floor=self.last_floor,
                current_capacity=current_capacity,
            )
        elif self.direction == Direction.DOWN and self.down.get(current_floor):
            self.take_people_down(
                floor=self.last_floor,
                current_capacity=current_capacity,
            )

    @property
    def current_capacity(self) -> int:
        return self.capacity - len(self.people_in_lift)

    def visit_floor(self, floor: int):
        self.floor_history.append(floor)

        self.people_get_out(floor)
        current_capacity = self.current_capacity

        if self.direction == Direction.UP:
            if self.up.get(floor) and current_capacity:
                self.take_people_up(
                    floor=floor,
                    current_capacity=current_capacity,
                )
            elif not len(self.up) and self.down.get(floor) and current_capacity:
                if any([k for k in self.down.keys() if k > floor]):
                    return

                self.take_people_down(
                    floor=floor,
                    current_capacity=current_capacity,
                )
        else:
            if self.down.get(floor) and current_capacity:
                self.take_people_down(
                    floor=floor,
                    current_capacity=current_capacity,
                )
            elif not len(self.down) and self.up.get(floor) and current_capacity:
                if any([k for k in self.up.keys() if k < floor]):
                    return

                self.take_people_up(
                    floor=floor,
                    current_capacity=current_capacity,
                )

    def people_get_out(self, floor: int):
        self.people_in_lift = [
            person for person in self.people_in_lift if person != floor
        ]

    def take_people_up(self, floor: int, current_capacity: int):
        self.people_in_lift += self.up[floor][:current_capacity]
        people_left = self.up[floor][current_capacity:]
        if people_left:
            self.up[floor] = people_left
        else:
            self.up.pop(floor)

    def take_people_down(self, floor: int, current_capacity: int):
        self.people_in_lift += self.down[floor][:current_capacity]
        people_left = self.down[floor][current_capacity:]
        if people_left:
            self.down[floor] = people_left
        else:
            self.down.pop(floor)


if __name__ == '__main__':
    tests = [
        [((), (), (5, 5, 5), (), (), (), ()), [0, 2, 5, 0], 5],
        [((), (), (1, 1), (), (), (), ()), [0, 2, 1, 0], 5],
        [((), (3,), (4,), (), (5,), (), ()), [0, 1, 2, 3, 4, 5, 0], 5],
        [((), (0,), (), (), (2,), (3,), ()), [0, 5, 4, 3, 2, 1, 0], 5],
        [((), (), (), (0, 0), ()), [0, 3, 0, 3, 0], 1],
        [[(), (), (4, 4), (), (2, 2), ()], [0, 2, 4, 2, 4, 2, 0], 1],
        [[(3, 3, 3, 3, 3, 3), (), (), (), (), (4, 4, 4, 4, 4, 4), ()], [0, 3, 5, 4, 0, 3, 5, 4, 0], 5],
        [((3,), (2,), (0,), (2,), (), (), (5,)), [0, 1, 2, 3, 6, 5, 3, 2, 0], 5],
    ]

    for _queues, _answer, _capacity in tests:
        lift = Dinglemouse(
            queues=_queues,
            capacity=_capacity,
        )
        assert lift.theLift() == _answer

    print('All tests passed')
