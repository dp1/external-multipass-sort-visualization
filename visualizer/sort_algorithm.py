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
        # Step 1. Create runs of F frames

        self.snapshot(f'Step 1: Create runs')

        for i in range(0, self.B, self.F):
            run_length = min(self.F, self.B - i)

            for j in range(run_length):
                self.buffer[j], self.relation[i+j] = self.relation[i+j], self.buffer[j]

            self.snapshot(f'Load {run_length} frames')
            self.sort_buffer(0, run_length)

            for j in range(run_length):
                self.buffer[j], self.relation[i+j] = self.relation[i+j], self.buffer[j]

            self.snapshot(f'Store sorted run {i // self.F}')

        # Step 2...N. Merge runs together

    def sort_buffer(self, start, end):
        items = []
        for i in range(start, end):
            items += self.buffer[i].data

        items.sort()

        for i in range(start, end):
            self.buffer[i].data = items[i * self.tuples_per_frame : (i+1) * self.tuples_per_frame]


    def snapshot(self, description = ''):
        self.steps.append(StateSnapshot(self.buffer, self.relation, description))
