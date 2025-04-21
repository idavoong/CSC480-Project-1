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

    


def ucs(cur, num_dirty, rows, cols, grid):
    pass
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

    algorithm = "depth-first"
    world_file = "example.txt"

    rows, cols, grid = read_file(world_file)
    start = find_start(grid)
    path = []

    if algorithm == "depth-first":
        dfs(start, rows, cols, grid, path)
        while path[len(path) - 1] != "V":
            path.pop()

        print(path)
