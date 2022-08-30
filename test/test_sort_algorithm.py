import unittest
import copy
from visualizer.sort_algorithm import Sort

class TestSort(unittest.TestCase):
    def test_different_sizes(self):
        for B in [2, 5, 10, 30, 100]:
            for F in [2, 5, 10, 100]:

                if F == 2 and B > 2: continue

                sort = Sort(B, F)
                original_data = copy.deepcopy(sort.relation)
                original_tuples = sum([x.data for x in original_data], [])
                # print(original_tuples)

                print(f'Running sort for B = {B}, F = {F}')
                # print(f'Data: {original_data}')

                sort.sort()

                # The buffer should contain F items
                self.assertEqual(len(sort.buffer), F)

                # The relation should contain B items
                self.assertEqual(len(sort.relation), B)

                # No data should be left in memory
                for frame in sort.buffer:
                    self.assertTrue(all([item.empty for item in frame.data]))

                # The relation should be sorted
                result_tuples = sum([x.data for x in sort.relation], [])
                self.assertEqual(result_tuples, sorted(original_tuples))

    def test_unable_to_merge(self):
        sort = Sort(10, 2)
        sort.sort()

        self.assertGreater(len(sort.steps), 0)
        self.assertEqual(sort.steps[-1].description, 'Unable to merge with only 2 frames')

if __name__ == '__main__':
    unittest.main()
