import random


def carve_from(maze, row, col, width, height):
    # Mark current as visited
    maze[row][col] = False

    # Get the directions to carve
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(directions)

    for direction in directions:
        if row + direction[0]*2 >= 1 and row + direction[0]*2 <= height-2 and \
            col + direction[1]*2 >= 1 and col + direction[1]*2 <= width-2 and \
            maze[row+direction[0]*2][col+direction[1]*2]:
            maze[row+direction[0]][col+direction[1]] = False
            carve_from(maze, row+direction[0]*2, col+direction[1]*2, width, height)


def get_maze(width, height, start_x, start_y):
    # For walls, False means broken, True means existing wall
    # For spaces, False means visited, True means non-visited
    # Nodes in row%2==0 or col%2==0 are walls
    if width % 2 != 1 or height % 2 != 1 or start_x % 2 != 1 or start_y % 2 != 1:
        raise ValueError("Cannot generate maze. width, height, start_x and start_y must be odd numbers")

    maze = [[True for row in range(height)] for col in range(width)]

    carve_from(maze, start_y, start_x, width, height)

    return maze
