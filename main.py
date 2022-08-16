from visualizer.sort_algorithm import Sort

def main():
    sort = Sort(B = 10, F = 5)
    sort.sort()

    for step in sort.steps:
        print(step)

if __name__ == '__main__':
    main()
