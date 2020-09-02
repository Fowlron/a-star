
class Node:
    def __init__(self, row, col, is_starting = False, is_target = False):
        self.row = row
        self.col = col
        self.is_passable = True
        self.parent = None
        self.in_open = False
        self.in_closed = False
        self.in_path = False
        self.is_starting = is_starting
        self.is_target = is_target

        self.f = 0
        self.g = 0
        self.h = 0

    def better_guess_than(self, node):
        if self.f == node.f:
            return self.h < node.h
        return self.f < node.f

    def set_parent(self, new_parent):
        self.parent = new_parent

    def calculate_f(self, g, target_node):
        self.g = g

        distance_row = abs(target_node.row - self.row)
        distance_col = abs(target_node.col - self.col)
        min_dist = min(distance_row, distance_col)
        max_dist = max(distance_row, distance_col)

        self.h = 14 * min_dist + 10 * (max_dist - min_dist)

        self.f = self.g + self.h

    def __repr__(self):
        return "<{}x{} f:{} g:{} h:{}>".format(self.row, self.col, self.f, self.g, self.h)


class Grid:
    def __init__(self, rows, cols, starting_node, target_node):
        self.rows = rows
        self.cols = cols
        self.nodes = [[Node(row, col) for col in range(cols)] for row in range(rows)]

        # Initialize the starting and target nodes
        self.starting_node = self.nodes[starting_node[0]][starting_node[1]]
        self.target_node = self.nodes[target_node[0]][target_node[1]]
        self.starting_node.is_starting = True
        self.target_node.is_target = True

        # Initialize the open and closed lists
        self.open = [self.starting_node]
        self.starting_node.in_open = True
        self.closed = []

        self.finished = False

    def set_starting(self, row, col):
        if self.nodes[row][col].is_target:
            return
        self.starting_node.is_starting = False
        self.starting_node.in_open = False
        self.starting_node = self.nodes[row][col]
        self.starting_node.is_starting = True
        self.starting_node.is_passable = True
        self.starting_node.in_open = True
        self.open = [self.starting_node]


    def set_target(self, row, col):
        if self.nodes[row][col].is_starting:
            return
        self.target_node.is_target = False
        self.target_node = self.nodes[row][col]
        self.target_node.is_target = True
        self.target_node.is_passable = True

    def do_iteration(self):
        if self.finished:
            return True

        # If open is empty, there's no path to target
        if len(self.open) == 0:
            self.finished = True
            return True

        # Find best guess node
        best_guess = self.open[0]
        for node in self.open[1:]:
            if node.better_guess_than(best_guess):
                best_guess = node
        
        # Remove best guess from open and add to closed
        self.open.remove(best_guess)
        best_guess.in_open = False
        self.closed.append(best_guess)
        best_guess.in_closed = True

        # If current is target node
        if best_guess is self.target_node:
            self.get_path()
            self.finished = True
            return True

        # Get best guess' neighbours
        # List of tuples in the format (node, additional cost)
        neighbours = self.get_neighbours(best_guess)

        for neighbour in neighbours:
            # If the neighbour is unpassable or in the closed list, skip it
            if not neighbour[0].is_passable or neighbour[0].in_closed:
                continue

            # If the current path to the neighbour is smaller than the previous one, or the neighbour wasn't in open
            if neighbour[0].g > best_guess.g + neighbour[1] or not neighbour[0].in_open:
                neighbour[0].calculate_f(best_guess.g + neighbour[1], self.target_node)
                neighbour[0].set_parent(best_guess)
                if not neighbour[0].in_open:
                    self.open.append(neighbour[0])
                    neighbour[0].in_open = True

        return False

    
    def get_neighbours(self, node):
        neighbours = []
        if node.row-1 >= 0 and node.col-1 >= 0 and \
            self.nodes[node.row-1][node.col].is_passable and self.nodes[node.row][node.col-1].is_passable:
            neighbours.append((self.nodes[node.row-1][node.col-1], 14))

        if node.row+1 < self.rows and node.col-1 >= 0 and \
            self.nodes[node.row+1][node.col].is_passable and self.nodes[node.row][node.col-1].is_passable:
            neighbours.append((self.nodes[node.row+1][node.col-1], 14))

        if node.row-1 >= 0 and node.col+1 < self.cols and \
            self.nodes[node.row-1][node.col].is_passable and self.nodes[node.row][node.col+1].is_passable:
            neighbours.append((self.nodes[node.row-1][node.col+1], 14))

        if node.row+1 < self.rows  and node.col+1 < self.cols and \
            self.nodes[node.row+1][node.col].is_passable and self.nodes[node.row][node.col+1].is_passable:
            neighbours.append((self.nodes[node.row+1][node.col+1], 14))

        if node.row+1 < self.rows:
            neighbours.append((self.nodes[node.row+1][node.col], 10))
        if node.row-1 >= 0:
            neighbours.append((self.nodes[node.row-1][node.col], 10))
        if node.col+1 < self.cols:
            neighbours.append((self.nodes[node.row][node.col+1], 10))
        if node.col-1 >= 0:
            neighbours.append((self.nodes[node.row][node.col-1], 10))


        return neighbours



    def add_walls(self, walls):
        for row, col in walls:
            self.nodes[row][col].is_passable = False


    def remove_walls(self, walls):
        for row, col in walls:
            self.nodes[row][col].is_passable = True


    def get_path(self):
        if self.target_node.parent == None:
            return []
        path = []
        current = self.target_node
        while current != None:
            path.append((current.row, current.col))
            current.in_path = True
            current = current.parent
        return path[::-1]


    def print_path(self):
        path = self.get_path()
        for row in range(self.rows):
            for col in range(self.cols):
                print('[{}]'.format('S' if self.nodes[row][col] is self.starting_node else
                                    'T' if self.nodes[row][col] is self.target_node else
                                    'W' if not self.nodes[row][col].is_passable else
                                    '-' if (row, col) in path else
                                    ' '
                ), end = '')
            print()
        print()


if __name__ == '__main__':
    g = Grid(10, 10, (1, 1), (8, 8))
    g.add_walls([(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8)])
    g.add_walls([(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9)])

    while not g.do_iteration():
        pass
    g.print_path()

    g = Grid(6, 6, (4, 4), (1, 1))
    g.add_walls([(1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)])
    while not g.do_iteration():
        pass
    g.print_path()