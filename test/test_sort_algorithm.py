import unittest
from visualizer.sort_algorithm import Sort

class TestSort(unittest.TestCase):
    def test_different_sizes(self):
        for B in [2, 5, 10, 100]:
            for F in [2, 5, 10, 100]:

                sort = Sort(B, F)
                original_data = sort.relation.copy()

                print(f'Running sort for B = {B}, F = {F}')
                print(f'Data: {original_data}')

                sort.sort()

                # The buffer should contain F items
                assert(len(sort.buffer) == F)
                # The relation should contain B items
                assert(len(sort.relation) == B)
                # No data should be left in memory
                assert(all([item.empty for item in sort.buffer]))
                # The relation should be sorted
                assert(sort.relation == sorted(original_data))
