import sys
from visualizer.sort_algorithm import Sort
from UI.UI import UI

def main():
    if '--no-gui' in sys.argv:
        B, F = map(int, input('B, F = ').replace(',',' ').split())
        sort = Sort(B, F)
        sort.sort()

        for step in sort.steps:
            print(step)
    else:
        ui = UI()

if __name__ == '__main__':
    main()
