from functools import total_ordering
from typing import List

@total_ordering
class Item:
    """
    A generic item to be sorted. If empty == True, represents an empty slot
    """
    def __init__(self, value = 0, empty = False):
        self.value = value
        self.empty = empty

    def __lt__(self, other): return self.value < other.value
    def __eq__(self, other): return self.value == other.value
    def __repr__(self): return f"{self.value}"

class SortStep:
    """
    A snapshot of the relation and buffer state
    """
    def __init__(self, buffer: List[Item], relation: List[Item], description = None):
        self.buffer = buffer.copy()
        self.relation = relation.copy()
        self.description = description

    def __repr__(self):
        return f'relation={self.relation} buffer={self.buffer}' \
            + f' ({self.description})' if self.description else ''
