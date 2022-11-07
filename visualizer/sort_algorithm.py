import random
from visualizer.data import Tuple, Frame, StateSnapshot
from copy import deepcopy

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

        self.snapshot('Step 1: Create runs')

        run_start, run_end = [], []
        for i in range(0, self.B, self.F):
            run_length = min(self.F, self.B - i)

            run_start.append(i)
            run_end.append(i + run_length)

            for j in range(run_length):
                self.buffer[j], self.relation[i+j] = self.relation[i+j], self.buffer[j]

            self.snapshot(f'Load {run_length} frames')
            self.sort_buffer(0, run_length)
            self.snapshot('Sort frames')

            for j in range(run_length):
                self.buffer[j], self.relation[i+j] = self.relation[i+j], self.buffer[j]

            self.snapshot(f'Store sorted run {i // self.F}')

        # Step 2...N. Merge runs together

        self.snapshot('Step 2: Merge runs')

        if self.F - 1 == 1 and len(run_start) > 1:
            self.snapshot('Unable to merge with only 2 frames')
            return

        while len(run_start) > 1:

            new_run_start, new_run_end = [], []

            for first_frame in range(0, len(run_start), self.F - 1):
                num_runs = min(self.F - 1, len(run_start) - first_frame)
                output_frames = []
                output_start = run_start[first_frame]

                new_run_start.append(run_start[first_frame])
                new_run_end.append(run_end[first_frame + num_runs - 1])

                # Load the first frame of each run
                for j in range(num_runs):
                    self.load_frame(run_start[first_frame + j], j)

                # Prepare output frame
                self.buffer[num_runs].clear()

                self.snapshot(f'Load first frames for {run_start[first_frame]} - {run_end[first_frame+num_runs-1]}')

                while True:
                    frame_id, t = self.next_min_tuple(0, num_runs)

                    # Merge completed
                    if t is None:
                        break

                    # Add tuple to output frame
                    self.buffer[self.F - 1].insert_tuple(t)

                    self.snapshot(f'Output min element {t}')

                    # Flush if needed
                    if self.buffer[self.F - 1].num_tuples() == self.tuples_per_frame:
                        output_frames.append(deepcopy(self.buffer[self.F - 1]))
                        self.buffer[self.F - 1].clear()

                        self.snapshot('Flush output frame')

                    # Load new input frame
                    if self.buffer[frame_id].num_tuples() == 0:
                        run_start[first_frame + frame_id] += 1
                        if run_start[first_frame + frame_id] < run_end[first_frame + frame_id]:
                            self.load_frame(run_start[first_frame + frame_id], frame_id)

                            self.snapshot('Load new input frame')

                # F-1 runs are sorted into one
                self.relation[output_start:output_start + len(output_frames)] = output_frames

            run_start, run_end = new_run_start, new_run_end

        self.snapshot('Done')


    def sort_buffer(self, start, end):
        items = []
        for i in range(start, end):
            items += self.buffer[i].data

        items.sort()

        for i in range(start, end):
            self.buffer[i].data = items[i * self.tuples_per_frame : (i+1) * self.tuples_per_frame]

    def next_min_tuple(self, start, end):
        idx, cur_best = -1, None
        for i,frame in enumerate(self.buffer[start:end]):
            t = frame.get_first_tuple()
            if t is None:
                continue

            if cur_best is None or t < cur_best:
                cur_best = t
                idx = i

        if idx == -1: return idx, None

        return idx, self.buffer[idx].pop_first_tuple()

    def load_frame(self, pos_in_relation, pos_in_buffer):
        self.buffer[pos_in_buffer], self.relation[pos_in_relation] = \
            self.relation[pos_in_relation], self.buffer[pos_in_buffer]

    def snapshot(self, description = ''):
        self.steps.append(StateSnapshot(self.buffer, self.relation, description))
