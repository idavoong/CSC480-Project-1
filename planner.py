import sys
import copy
import heapq
from itertools import permutations


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


def reverse_path(path):
    temp = path[::-1] # reverse path
    reversed_path = []

    for p in temp: # flip directions
        match p:
            case 'N':
                reversed_path.append('S')
            case 'E':
                reversed_path.append('W')
            case 'S':
                reversed_path.append('N')
            case 'W':
                reversed_path.append('E')
    return reversed_path


def start_to_end(start, end, grid):
    costs = copy.deepcopy(grid)
    costs[start[0]][start[1]] = 0
    explore = [start]
    heapq.heapify(explore)

    while len(explore) > 0:
        cur = heapq.heappop(explore)
        row, col = cur[0], cur[1]

        neighbors = {
            'N': (row - 1, col),
            'E': (row, col + 1),
            'S': (row + 1, col),
            'W': (row, col - 1)
        }

        for n in neighbors.keys():
            r = neighbors[n][0]
            c = neighbors[n][1]
            if 0 <= r < len(costs) and 0 <= c < len(costs[r]):
                if isinstance(costs[r][c], int) and costs[r][c] > costs[row][col] + 1: # replace cost if this path is cheaper
                    costs[r][c] = costs[row][col] + 1
                    heapq.heappush(explore, (r, c))
                elif costs[r][c] == '_' or costs[r][c] == '*':
                    costs[r][c] = costs[row][col] + 1
                    heapq.heappush(explore, (r, c))

    reversed_path = []
    row, col = end[0], end[1]
    while costs[row][col] != 0:
        neighbors = {
            'N': (row - 1, col),
            'E': (row, col + 1),
            'S': (row + 1, col),
            'W': (row, col - 1)
        }

        for n in neighbors.keys():
            r = neighbors[n][0]
            c = neighbors[n][1]
            if 0 <= r < len(costs) and 0 <= c < len(costs[r]):
                if costs[r][c] == costs[row][col] - 1:
                    row, col = r, c
                    reversed_path.append(n)
                    break

    path = reverse_path(reversed_path)
    total_cost = len(path)

    return path, reversed_path, total_cost


def ucs(cur, rows, cols, grid):
    dirty_cells = dirty_coords(grid)
    costs = {}
    paths = {}

    i = 0
    while i < len(dirty_cells):
        j = i + 1
        while j < len(dirty_cells):
            cost = start_to_end(dirty_cells[i], dirty_cells[j], grid)
            costs[(dirty_cells[i], dirty_cells[j])] = cost[2]
            costs[(dirty_cells[j], dirty_cells[i])] = cost[2]
            paths[(dirty_cells[i], dirty_cells[j])] = cost[0]
            paths[(dirty_cells[j], dirty_cells[i])] = cost[1]
            j += 1
        i += 1

    print(costs)

    # perms = list(permutations(dirty_cells))
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
        ucs(start, rows, cols, grid)