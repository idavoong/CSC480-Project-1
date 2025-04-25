import sys
import copy
import heapq
from itertools import permutations
from collections import defaultdict
import json


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
    costs = copy.deepcopy(grid) # make a copy of the grid to store costs of each cell
    costs[start[0]][start[1]] = 0 # start cell cost is 0
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
            if 0 <= r < len(costs) and 0 <= c < len(costs[r]): # check if cell is in bounds
                if isinstance(costs[r][c], int) and costs[r][c] > costs[row][col] + 1: # replace cost if this path is cheaper
                    costs[r][c] = costs[row][col] + 1
                    heapq.heappush(explore, (r, c))
                elif costs[r][c] == '_' or costs[r][c] == '*' or costs[r][c] == '@': # check if cell is empty, dirty, or start
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

        no_path = False

        for n in neighbors.keys(): # need a case where the surrounding cells are obstacles/dirty
            r = neighbors[n][0]
            c = neighbors[n][1]
            if 0 <= r < len(costs) and 0 <= c < len(costs[r]):
                if isinstance(costs[r][c], int) and costs[r][c] == costs[row][col] - 1:
                    row, col = r, c
                    reversed_path.append(n)
                    break
                elif n == 'W':
                    no_path = True
            elif n == 'W':
                no_path = True
        
        if no_path:
            break

    path = reverse_path(reversed_path)
    total_cost = len(path)

    if total_cost == 0: # this means that the cell is unreachable
        total_cost = float('inf')

    return path, reversed_path, total_cost


def ucs(cur, rows, cols, grid):
    dirty_cells = dirty_coords(grid)
    dirty_cells.insert(0, cur) # start cell will be labeled as A
    named_cells = {}
    
    for i in range(len(dirty_cells)):
        named_cells[dirty_cells[i]] = f"{chr(65 + i)}"

    costs = defaultdict(lambda: defaultdict(int))
    paths = defaultdict(lambda: defaultdict(int))

    i = 0
    while i < len(dirty_cells):
        j = i + 1
        while j < len(dirty_cells):
            cost = start_to_end(dirty_cells[i], dirty_cells[j], grid)
            cell_i = named_cells[dirty_cells[i]]
            cell_j = named_cells[dirty_cells[j]]

            costs[cell_i][cell_j] = cost[2]
            costs[cell_j][cell_i] = cost[2]
            paths[cell_i][cell_j] = cost[0]
            paths[cell_j][cell_i] = cost[1]
            j += 1
        i += 1

    reachable = ['A']
    for cell in costs['A'].keys():
        if costs['A'][cell] != float('inf'):
            reachable.append(cell)

    reachable.remove('A')
    if len(reachable) == 0:
        print("No reachable dirty cells")
        return []
    
    perms = list(permutations(reachable))

    min_cost = float('inf')
    min_path = []
    for perm in perms:
        cost = 0
        path = []
        for i in range(len(perm) - 1):
            # print(perm[i], perm[i + 1])
            # print(costs[perm[i]][perm[i + 1]])
            cost += costs[perm[i]][perm[i + 1]]
            path += paths[perm[i]][perm[i + 1]]

        cost += costs['A'][perm[0]] # add cost from start to first dirty cell
        path = paths['A'][perm[0]] + path # add path from start to first dirty cell

        if cost < min_cost:
            min_cost = cost
            min_path = path

    print(min_cost)
    print(min_path)

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
    world_file = "test4.txt"

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
        # dirty_cells = dirty_coords(grid)
        # path = start_to_end(start, dirty_cells[2], grid)
        # print(path)
