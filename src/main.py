import time

from src.map import Map
from src.solutions.solution1 import solution1
from src.solutions.solution2 import solution2


def main():
    flat = Map('rooms.txt')

    print("\nSOLUTION 1")
    start_time = time.time()
    solution1(flat)
    print("--- %s seconds ---" % (time.time() - start_time))

    print("\nSOLUTION 2")
    start_time = time.time()
    solution2(flat)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
