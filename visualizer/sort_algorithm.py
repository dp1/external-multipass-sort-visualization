import random
from visualizer.data import Tuple, Frame, StateSnapshot

class Sort:
    """
    Implements the external multipass sort algorithm
    """
    def __init__(self, B: int, F: int):
        self.B = B
        self.F = F
        self.tuples_per_frame = 4

        self.steps = []
        self.buffer = []
        self.relation = []

        for _ in range(self.F):
            data = [Tuple(empty = True) for _ in range(self.tuples_per_frame)]
            self.buffer.append(Frame(data))

        values = list(range(self.B * self.tuples_per_frame))
        random.shuffle(values)

        for i in range(self.B):
            data = [Tuple(value = values[i * self.tuples_per_frame + j]) for j in range(self.tuples_per_frame)]
            self.relation.append(Frame(data))

    """
    Sort the relation data, creating a series of StateSnapshot snapshots that the GUI will later visualize
    """
    def sort(self):
        for i in range(10):
            self.steps.append(StateSnapshot(self.buffer, self.relation, f'step {i}'))
            random.shuffle(self.relation)

        values = []
        for x in self.relation:
            values += x.data
        self.relation.clear()

        values.sort()

        for i in range(self.B):
            data = [values[i * self.tuples_per_frame + j] for j in range(self.tuples_per_frame)]
            self.relation.append(Frame(data))
