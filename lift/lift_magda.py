class Dinglemouse(object):

    def __init__(self, queues, capacity):
        self.queues = [list(q) for q in queues]
        self.capacity = capacity
        self.people_inside = []
        self.direction = "up"
        self.current_stop = 0

    def theLift(self):
        lift_stops = [0]

        while not self.finish():
            self.people_exit()
            self.people_enter()

            next_stop = self.get_next_stop()
            if next_stop is not None:
                self.current_stop = next_stop
                lift_stops.append(self.current_stop)

        if lift_stops[-1] != 0:
            lift_stops.append(0)
        return lift_stops

    def finish(self):
        if self.people_inside:
            return False
        return all([len(set(q)) == 1 and idx == q[0] for idx, q in enumerate(self.queues) if len(q) > 0])

    def people_exit(self):
        people_getting_off = []
        people_staying = []
        for person in self.people_inside:
            if person == self.current_stop:
                people_getting_off.append(person)
            else:
                people_staying.append(person)

        self.queues[self.current_stop] += people_getting_off
        self.people_inside = people_staying

        return len(people_getting_off)

    def people_enter(self):
        free_spots = self.capacity - len(self.people_inside)
        if self.direction == "up":
            queue = [person for person in self.queues[self.current_stop] if person > self.current_stop]
        else:
            queue = [person for person in self.queues[self.current_stop] if person < self.current_stop]

        while free_spots and queue:
            person = queue.pop(0)
            self.queues[self.current_stop].remove(person)
            self.people_inside.append(person)
            free_spots -= 1

    def get_next_stop(self):
        queue_down = [[p for p in queue if p < idx] for idx, queue in enumerate(self.queues)]
        queue_up = [[p for p in queue if p > idx] for idx, queue in enumerate(self.queues)]
        if self.direction == "up":
            queue = [i for i, queue in enumerate(queue_up[self.current_stop + 1:], start=self.current_stop + 1) if
                     len(queue) > 0]
        else:
            queue = [i for i, queue in enumerate(queue_down[:self.current_stop]) if len(queue) > 0]

        queue += self.people_inside
        if queue:
            if len(queue) > 1:
                if self.direction == "up":
                    return min(queue)
                else:
                    return max(queue)
            else:
                return queue[0]
        if not self.people_inside:
            if self.direction == "up":
                for i, queue in enumerate(queue_down[self.current_stop + 1:][::-1], start=1):
                    if len(queue) > 0:
                        self.change_direction()
                        return len(self.queues) - i
            else:
                for i, queue in enumerate(queue_up[:self.current_stop]):
                    if len(queue) > 0:
                        self.change_direction()
                        return i

        self.change_direction()
        return None

    def change_direction(self):
        self.direction = "down" if self.direction == "up" else "up"
