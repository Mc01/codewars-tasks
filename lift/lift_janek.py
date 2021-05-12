class Dinglemouse(object):

    def __init__(self, queues, capacity):
        self.queues = [list(q) for q in queues]
        self.capacity = capacity
        self.occupied_space = 0
        self.current_floor = 0
        self.direction = 1  # 1 for up, -1 for down
        self.lift_content = []
        self.end = False
        self.visited_floors = [0]

    def theLift(self):
        self.lift_and_queues_empty()
        while not self.end:
            self.service_the_floor()
            self.current_floor = self.pick_next_floor()
            if self.current_floor is None and self.visited_floors[-1] != 0:
                self.visited_floors.append(0)
            elif not (self.visited_floors[-1] == 0 and not self.current_floor):
                self.visited_floors.append(self.current_floor)
        return self.visited_floors

    def service_the_floor(self):
        self.empty_the_lift()
        self.pick_from_queue()

    def pick_from_queue(self):
        queue = self.queues[self.current_floor]
        incomers = []
        for q in queue:
            if self.capacity == self.occupied_space:
                break
            elif q > self.current_floor and self.direction == 1 or q < self.current_floor and self.direction == -1 or (
                    self.direction == 1 and not self.someone_to_upper_floor()) or (
                    self.direction == -1 and not self.someone_to_lower_floor()):
                incomers.append(q)
                self.occupied_space += 1
        self.delete_from_queue(queue, incomers)
        self.lift_content.extend(incomers)

    def delete_from_queue(self, queue, incomers):
        for i in incomers:
            queue.remove(i)

    def empty_the_lift(self):
        self.lift_content = list(filter(lambda x: x != self.current_floor, self.lift_content))
        self.occupied_space = len(self.lift_content)

    def lift_and_queues_empty(self):
        if not any(q for q in self.queues) and not self.lift_content:
            self.end = True
        else:
            self.end = False

    def someone_to_upper_floor(self):
        """
        Return True if there is anyone who is to be picked from upper floors
        or someone who wants to go up in the lift
        """
        return any(q > self.current_floor for q in self.lift_content) or any(self.queues[self.current_floor + 1:])

    def someone_to_lower_floor(self):
        """
        Return True if there is anyone who is to be picked from lower floors
        or someone who wants to go down in the lift
        """
        return any(q < self.current_floor for q in self.lift_content) or any(self.queues[:self.current_floor])

    def pick_direction(self):
        """
        Set direction of the lift from this point.
        If lift going up and there is someone to be left upper
        or lift is going down and there is no one to be left lower, but there is someone to be left upper -> go up
        """

        if self.someone_to_upper_floor() and (
                self.direction == 1 or (
                not self.someone_to_lower_floor() and self.direction == -1
        )
        ):
            # go up
            self.direction = 1
        else:
            # go down
            self.direction = -1

    def find_next_floor(self):
        """
        Find the closest floor to stop in given direction
        """
        i = 1
        floor = self.current_floor
        while 0 <= floor < len(self.queues):
            self.lift_and_queues_empty()
            floor = self.current_floor + i * self.direction
            if floor in self.lift_content or (self.queues[floor:] and any(
                    q * self.direction > floor * self.direction for q in self.queues[floor])):
                return floor
            i += 1
        # pick the last or the first floor with someone there
        if self.direction == 1:
            for floor in range(len(self.queues) - 1, 0, -1):
                if self.queues[floor]:
                    return floor
        else:
            for floor in range(len(self.queues)):
                if self.queues[floor]:
                    return floor

    def pick_next_floor(self):
        self.pick_direction()  # make sure that direction is ok
        return self.find_next_floor()
