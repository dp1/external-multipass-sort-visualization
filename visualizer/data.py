from functools import total_ordering
from copy import copy, deepcopy
from typing import List

@total_ordering
class Tuple:
    """
    A tuple of the relationship. If empty == True, represents an empty slot
    """
    def __init__(self, value = 0, empty = False):
        self.value = value
        self.empty = empty

    def __lt__(self, other): return self.value < other.value
    def __eq__(self, other): return self.value == other.value
    def __repr__(self): return '-' if self.empty else str(self.value)

class Frame:
    """
    Fixed size frame
    """
    def __init__(self, data: List[Tuple]):
        self.data = data

    def clear(self):
        for t in self.data:
            t.empty = True

    def num_tuples(self):
        ctr = 0
        for t in self.data:
            if not t.empty:
                ctr += 1
        return ctr

    def get_first_tuple(self):
        for t in self.data:
            if not t.empty:
                return t
        return None

    def pop_first_tuple(self):
        for t in self.data:
            if not t.empty:
                res = deepcopy(t)
                t.empty = True
                return res
        return None

    def insert_tuple(self, x):
        for i,t in enumerate(self.data):
            if t.empty:
                self.data[i] = deepcopy(x)
                break

    def __repr__(self): return str(self.data)
    def __len__(self): return len(self.data)

class StateSnapshot:
    """
    A snapshot of the relation and buffer state
    """
    def __init__(self, buffer: List[Frame], relation: List[Frame], description = None):
        self.buffer = [deepcopy(f) for f in buffer]
        self.relation = [deepcopy(f) for f in relation]
        self.description = description

    def __repr__(self):
        return f'relation={self.relation}\n' \
            + f'buffer={self.buffer}\n' \
            + (f' ({self.description})' if self.description else '') \
            + '\n'
