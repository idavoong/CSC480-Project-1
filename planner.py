import sys


def read_file(file):
    with open(file, 'r') as file:
        rows = int(file.readline().strip())
        cols = int(file.readline().strip())

        grid = []
        for _ in range(cols):
            grid.append(list(file.readline().strip()))

    return rows, cols, grid


def find_start(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '@':
                return r, c
            

def ucs(start, rows, cols, grid):
    pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py <algorithm> <world-file>")
        sys.exit(1)
    
    algorithm = sys.argv[1]
    world_file = sys.argv[2]

    rows, cols, grid = read_file(world_file)
    start = find_start(grid)

    print(grid)
