import sys
import copy
import heapq


def read_file(file):
    with open(file, 'r', encoding='utf-16') as file:
        cols = int(file.readline().strip())
        rows = int(file.readline().strip())

        grid = []
        for _ in range(rows):
            grid.append(list(file.readline().strip()))

    return rows, cols, grid


def find_start(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '@':
                return r, c
            

def dfs(cur, rows, cols, grid, path=[]):
    row, col = cur[0], cur[1]
    part_of_path = False

    if grid[row][col] == '*':
        path.append("V")
        part_of_path = True

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
                path.append(n)
                part = dfs(neighbors[n], rows, cols, grid, path)
                if part:
                    part_of_path = True
                    match n: # backtracking
                        case 'N':
                            path.append('S')
                        case 'E':
                            path.append('W')
                        case 'S':
                            path.append('N')
                        case 'W':
                            path.append('E')
                else:
                    path.pop()

    return part_of_path


def dirty_coords(grid):
    dirty = []
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '*':
                dirty.append((r, c))
    return dirty


def start_to_end(start, end, grid):
    costs = copy.deepcopy(grid)
    dist_to_end = abs(start[0] - end[0]) + abs(start[1] - end[1]) * -1 # negative for max heap
    explore = [dist_to_end]
    heapq.heapify(explore)

    while len(explore) > 0:
        cur = heapq.heappop(explore)
        row, col = cur[0], cur[1]

        if costs[row][col] == 'v':
            continue

        costs[row][col] = 'v'

        neighbors = {
            'N': (row - 1, col),
            'E': (row, col + 1),
            'S': (row + 1, col),
            'W': (row, col - 1)
        }

        for n in neighbors.keys():
            r = neighbors[n][0]
            c = neighbors[n][1]
            if 0 <= r < len(grid) and 0 <= c < len(grid[r]):
                if grid[r][c] != '#' and grid[r][c] != 'v':
                    dist_to_end = abs(r - end[0]) + abs(c - end[1]) * -1
                    heapq.heappush(explore, dist_to_end)



def ucs(cur, rows, cols, grid):
    dirty_cells = dirty_coords(grid)

    # i = 0
    # while i < len(dirty_cells):
    #     j = i + 1
    #     while j < len(dirty_cells):
    #         cost = a_star(dirty_cells[i], dirty_cells[j], grid)
    #         j += 1
    #     i += 1
    """
    find cost of going from one dirty cell to another
    find optimal path to clean all dirty cells 
    using all possible combinations of dirty cells and start
    """


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: python3 planner.py <algorithm> <world-file>")
    #     # python3 planner.py depth-first example.txt
    #     # python3 planner.py uniform-cost example.txt
    #     sys.exit(1)
    
    # algorithm = sys.argv[1]
    # world_file = sys.argv[2]

    algorithm = "uniform-cost"
    world_file = "test1.txt"

    rows, cols, grid = read_file(world_file)
    start = find_start(grid)
    path = []

    if algorithm == "depth-first":
        dfs(start, rows, cols, grid, path)
        while path[len(path) - 1] != "V":
            path.pop()

        print(path)
    elif algorithm == "uniform-cost":
        dirty = dirty_coords(grid)
        print(dirty)
