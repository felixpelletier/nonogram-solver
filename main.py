from solver import solve
from fetcher import get_random_nonogram, SIZE_25_25
import time

if __name__ == "__main__":
    times = []
    for i in range(100):
        problem = get_random_nonogram(SIZE_25_25)
        start_time = time.time()
        solved_grid = solve(problem)
        total_time = time.time() - start_time

        times.append(total_time)
        average_time = sum(times)/len(times)
        print(average_time)

        print(solved_grid)
        if not solved_grid.is_solved():
            print("BUG DETECTED")
            break
