# a-star
A python A* pathfinding implementation. This was meant as a fun time-waster project and isn't meant to be efficient or show correct code practices.

![example](https://github.com/Fowlron/a-star/blob/master/example.png?raw=true)

## astar.py

astar.py contains the actual pathfinding algorithm implementation. Note: nothing in this file does argument type verification, so using the wrong parameter types will likely crash.

To use the A* algorithm, simply create a `Grid` object, passing it the number of rows and columns, as well as 2 tuples with the `(row, col)` coordinates of the starting and target nodes. You can add walls through the `add_walls` method, sending a list of `(row, col)` coordinates. You can then call `do_iteration` until it returns True, meaning either the shortest path was found, or no path exists. You can get that path through `get_path`. Example code:

```
g = Grid(6, 6, (4, 4), (1, 1))
g.add_walls([(1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)])
while not g.do_iteration():
    pass
print(g.get_path())
g.print_path()
```

## mazegen.py

mazegen.py contains an implementation of the recursive backtracking algorithm for generating mazes. You can get a maze by calling `get_maze` with the width and height of the maze, followed by the x and y coordinates of the starting point. It will return a boolean 2d list. True means wall, False means no wall.

## astargui.py

astargui.py contains the gui visualization for the algorithm. It depends on pygame and tkinter. Note: You can only create mazes if the width and height are odd numbers.

Settings:
- Width: width of the window in pixels
- Height: height of the window in pixels
- Rows: number of rows in the grid
- Columns: number of columns in the grid
- Solve Speed: number of steps per second when stepping until finished. 0 means to not show intermediate steps and jump to the solved grids.

Mouse Controls:
- Drag Start or Target nodes to move them
- Drag from a blank node to draw walls
- Drag from a wall node to remove walls

Keyboard Controls:
- Space - do a step of A*
- Enter - do A* steps until algorithm is finished
- M - reset grid and generate a random maze
- R - reset grid