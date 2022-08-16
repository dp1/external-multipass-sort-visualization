import random
from visualizer.data import Item, SortStep

class Sort:
    """
    Implements the external multipass sort algorithm
    """
    def __init__(self, B: int, F: int):
        self.B = B
        self.F = F
        self.steps = []
        self.buffer = [Item(empty = True) for _ in range(self.F)]
        self.relation = [Item(value = i) for i in range(self.B)]

        random.shuffle(self.relation)

    """
    Sort the relation data, creating a series of SortStep snapshots that the GUI will later visualize
    """
    def sort(self):
        for i in range(10):
            self.steps.append(SortStep(self.buffer, self.relation, f'step {i}'))
            random.shuffle(self.relation)

        self.relation.sort()
