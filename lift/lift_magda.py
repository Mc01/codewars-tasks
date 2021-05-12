class Dinglemouse(object):
    def __init__(self, queues, capacity):
        self.queues = [list(q) for q in queues]
        self.capacity = capacity
        self.people_inside = []
    def theLift(self):
        lift_stops = [0]
        current_stop = 0
        direction = "up"
        while not self.finish():
            self.people_exit(current_stop)
            self.people_enter(current_stop, direction)
            next_stop, direction = self.get_next_stop(current_stop, direction)
            if next_stop is not None and next_stop != current_stop:
                current_stop = next_stop
                lift_stops.append(current_stop)
        if lift_stops[-1] != 0:
            lift_stops.append(0)
        return lift_stops
    def finish(self):
        if self.people_inside:
            return False
        return all([len(set(q)) == 1 and idx == q[0] for idx, q in enumerate(self.queues) if len(q) > 0])
    def people_exit(self, current_stop):
        people_getting_off = []
        people_staying = []
        for person in self.people_inside:
            if person == current_stop:
                people_getting_off.append(person)
            else:
                people_staying.append(person)
        self.queues[current_stop] += people_getting_off
        self.people_inside = people_staying
    def people_enter(self, current_stop, direction):
        free_spots = self.capacity - len(self.people_inside)
        if direction == "up":
            queue = [person for person in self.queues[current_stop] if person > current_stop]
        else:
            queue = [person for person in self.queues[current_stop] if person < current_stop]
        while free_spots and queue:
            person = queue.pop(0)
            self.queues[current_stop].remove(person)
            self.people_inside.append(person)
            free_spots -= 1
    def get_next_stop(self, current_stop, direction):
        next_stop = None
        queue_down = [idx for idx, queue in enumerate(self.queues) if any([p < idx for p in queue])]
        queue_up = [idx for idx, queue in enumerate(self.queues) if any([p > idx for p in queue])]
        if not self.people_inside:
            if direction == "up":
                next_stop = min(queue_up) if queue_up else max(queue_down) if queue_down else None
            else:
                next_stop = max(queue_down) if queue_down else min(queue_up) if queue_up else None
        else:
            if direction == "up":
                queue_stop = min(queue_up) if queue_up else None
                inside_wanted_stop = min(self.people_inside)
                if queue_stop is None and inside_wanted_stop is not None:
                    next_stop = inside_wanted_stop
                elif queue_stop is not None and inside_wanted_stop is not None:
                    next_stop = min(queue_stop, inside_wanted_stop)
            else:
                queue_stop = max(queue_down) if queue_down else None
                inside_wanted_stop = max(self.people_inside)
                if queue_stop is None and inside_wanted_stop is not None:
                    next_stop = inside_wanted_stop
                elif queue_stop is not None and inside_wanted_stop is not None:
                    next_stop = max(queue_stop, inside_wanted_stop)
        # change direction
        if next_stop is None or next_stop == current_stop:
            direction = "down" if direction == "up" else "up"
        if next_stop == current_stop and len(self.people_inside) == self.capacity:
            if direction == "down":
                next_stop = max(queue_stop, inside_wanted_stop)
            else:
                next_stop = min(queue_stop, inside_wanted_stop)
        return next_stop, direction
