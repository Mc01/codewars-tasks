class Dinglemouse(object):

    def __init__(self, queues, capacity):
        self.queues = [list(queue) for queue in queues]
        self.capacity = capacity

    def theLift(self):
        max_floor = len(self.queues) - 1
        result = [0]
        current_floor = 0
        people_inside_lift = []
        up_direction = True
        while True:
            if current_floor == 0:
                no_more_waiting_people = True
                for people_on_floor in self.queues:
                    if len(people_on_floor) > 0:
                        no_more_waiting_people = False
                        break
                if no_more_waiting_people:
                    break
            stopped_on_the_floor = False
            if current_floor in people_inside_lift:
                people_inside_lift = [person for person in people_inside_lift if person != current_floor]
                stopped_on_the_floor = True
            if len(self.queues[current_floor]) > 0:
                people_to_remove_from_queue = []
                for person in self.queues[current_floor]:
                    if current_floor == max_floor:
                        stopped_on_the_floor = True
                        if len(people_inside_lift) < self.capacity:
                            people_inside_lift.append(person)
                            people_to_remove_from_queue.append(person)
                    elif current_floor == 0:
                        stopped_on_the_floor = True
                        if len(people_inside_lift) < self.capacity:
                            people_inside_lift.append(person)
                            people_to_remove_from_queue.append(person)
                    elif up_direction:
                        if person > current_floor:
                            stopped_on_the_floor = True
                            if len(people_inside_lift) < self.capacity:
                                people_inside_lift.append(person)
                                people_to_remove_from_queue.append(person)
                    else:
                        if person < current_floor:
                            stopped_on_the_floor = True
                            if len(people_inside_lift) < self.capacity:
                                people_inside_lift.append(person)
                                people_to_remove_from_queue.append(person)
                for person in people_to_remove_from_queue:
                    self.queues[current_floor].remove(person)
            if stopped_on_the_floor and current_floor != result[-1]:
                stopped_on_the_floor = False
                result.append(current_floor)
            if up_direction:
                if current_floor == max_floor:
                    up_direction = False
                    current_floor -= 1
                else:
                    current_floor += 1
            else:
                if current_floor == 0:
                    up_direction = True
                    current_floor += 1
                else:
                    current_floor -= 1
        if result[-1] != 0:
            result.append(0)
        return result
