import sys


def read_file(file):
    with open(file, 'r') as file:
        cols = int(file.readline().strip())
        rows = int(file.readline().strip())

        grid = []
        for _ in range(cols):
            grid.append(list(file.readline().strip()))

    return rows, cols, grid


def find_start(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '@':
                return r, c
            

def num_dirty(grid):
    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '*':
                count += 1
    return count
            

def dfs(cur, num_dirty, rows, cols, grid):
    row, col = cur[0], cur[1]

    if grid[row][col] == '*':
        print("V")
        num_dirty -= 1
    
    grid[row][col] = 'v' # v for visited

    neighbors = {
        'N': (row - 1, col),
        'E': (row, col + 1),
        'S': (row + 1, col),
        'W': (row, col - 1)
    }

    for n in neighbors.keys():
        r = neighbors[n][0]
        c = neighbors[n][1]
        if 0 <= r < rows and 0 <= c < cols:
            if grid[r][c] != '#' and grid[r][c] != 'v':
                print(n, r, c)
                num_dirty = dfs(neighbors[n], num_dirty, rows, cols, grid)
                if num_dirty:
                    match n:
                        case 'N':
                            print('S')
                        case 'E':
                            print('W')
                        case 'S':
                            print('N')
                        case 'W':
                            print('E')

    return num_dirty


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py <algorithm> <world-file>")
        # python3 planner.py depth-first example.txt
        # python3 planner.py uniform-cost example.txt
        sys.exit(1)
    
    algorithm = sys.argv[1]
    world_file = sys.argv[2]

    rows, cols, grid = read_file(world_file)
    start = find_start(grid)
    dirty_count = num_dirty(grid)

    if sys.argv[1] == "depth-first":
        dfs(start, dirty_count, rows, cols, grid)
