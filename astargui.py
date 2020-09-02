import pygame
import tkinter as tk

import astar
import mazegen


class GUI:
    def __init__(self, width, height, rows, cols, tick_speed=30, show_numbers=False):
        self.grid = astar.Grid(rows, cols, (1, 1), (rows - 2, cols - 2))
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height

        # Autosolving vars
        self.solving = False
        self.tick_speed = tick_speed

        # Make rows and cols as big as possible while still squares
        self.node_size = min(height/rows, width/cols)

        # Calculate the location of the first row and col to center them on the screen
        self.base_row_loc = (height - self.node_size * rows) / 2
        self.base_col_loc = (width - self.node_size * cols) / 2

        # Mouse interaction variables
        self.dragging = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.just_clicked = False
        self.can_interact = True
        self.dragging_starting = False
        self.dragging_target = False
        self.dragging_passable = False
        self.dragging_wall = False

        self.show_numbers = show_numbers


    def start(self):
        # Initialize the screen
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        done = False

        # Prepare the fonts
        self.big_font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 20)

        # Main life cycle
        while not done:
            for event in pygame.event.get():
                if self.can_interact:
                    # Mouse events
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.dragging = True
                            self.just_clicked = True
                            self.mouse_x, self.mouse_y = event.pos
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            self.dragging = False
                    elif event.type == pygame.MOUSEMOTION:
                        if self.dragging:
                            self.mouse_x, self.mouse_y = event.pos
                    # Make a Maze
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                        try:
                            maze = mazegen.get_maze(self.cols, self.rows, 1, 1)
                            self.grid = astar.Grid(self.rows, self.cols, (1, 1), (self.rows - 2, self.cols - 2))
                            walls = []
                            for row in range(self.rows):
                                for col in range(self.cols):
                                    if maze[row][col]:
                                        walls.append((row, col))
                            self.grid.add_walls(walls)
                        except ValueError as e:
                            print(e)
                    # Solve
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.can_interact = False
                        if self.tick_speed == 0:
                            while not self.grid.do_iteration():
                                pass
                        else:
                            self.solving = True
                # Do one step
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.solving:
                    self.can_interact = False
                    self.grid.do_iteration()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.grid = astar.Grid(self.rows, self.cols, (1, 1), (self.rows - 2, self.cols - 2))
                    self.solving = False
                    self.dragging = False
                    self.mouse_x = 0
                    self.mouse_y = 0
                    self.just_clicked = False
                    self.can_interact = True
                    self.dragging_starting = False
                    self.dragging_target = False
                    self.dragging_passable = False
                    self.dragging_wall = False

                # Close
                elif event.type == pygame.QUIT:
                    done = True

            # Handle Mouse
            self.handle_mouse()

            if self.solving:
                self.clock.tick(self.tick_speed)
                if self.grid.do_iteration():
                    self.solving = False
            else:
                self.clock.tick(30)

            # Draw the nodes
            for row in range(self.rows):
                for col in range(self.cols):
                    self.draw_node(row, col)

            pygame.display.flip()


    def handle_mouse(self):
        if self.can_interact and self.dragging:
            row, col = self.get_mouse_node()
            # Update Flags
            if self.just_clicked:
                self.dragging_starting = False
                self.dragging_target = False
                self.dragging_passable = False
                self.dragging_wall = False
                if self.grid.nodes[row][col].is_starting:
                    self.dragging_starting = True
                elif self.grid.nodes[row][col].is_target:
                    self.dragging_target = True
                elif not self.grid.nodes[row][col].is_passable:
                    self.dragging_wall = True
                else:
                    self.dragging_passable = True
                self.just_clicked = False

            # Dragging the starting or target node
            if self.dragging_starting:
                if not self.grid.nodes[row][col].is_starting:
                    self.grid.set_starting(row, col)
            if self.dragging_target:
                if not self.grid.nodes[row][col].is_target:
                    self.grid.set_target(row, col)
            
            # Dragging on an empty node
            if self.dragging_passable:
                if self.grid.nodes[row][col].is_passable:
                    self.grid.add_walls([(row, col)])
            
            # Dragging on a wall
            if self.dragging_wall:
                if not self.grid.nodes[row][col].is_passable:
                    self.grid.remove_walls([(row, col)])

    def get_mouse_node(self):
        return (max(0, int((self.mouse_y-self.base_row_loc) // self.node_size)),
                max(0, int((self.mouse_x-self.base_col_loc) // self.node_size)))


    def draw_outlined_rec(self, color, x, y, width, height, outline_width, outline_color):
        pygame.draw.rect(self.screen, outline_color, pygame.Rect(x, y, width, height))
        pygame.draw.rect(self.screen, color, pygame.Rect(x+outline_width, y+outline_width, width - 2*outline_width, height - 2*outline_width))


    def draw_node(self, row, col, outline_width = 1, show_numbers = False):
        node = self.grid.nodes[row][col]

        # Pick the color
        color = (230, 230, 230)
        if not node.is_passable:    color = (20, 20, 20)
        if node.in_open:            color = (78, 217, 39)
        if node.in_closed:          color = (222, 9, 9)
        if node.in_path:            color = (11, 224, 214)
        if node.is_starting:        color = (235, 231, 16)
        if node.is_target:          color = (148, 146, 6)

        # Draw the rectangle
        x = self.base_col_loc + col*self.node_size
        y = self.base_row_loc + row*self.node_size
        self.draw_outlined_rec(color, x, y, self.node_size, self.node_size, outline_width, (0, 0, 0))

        # Draw the text
        if node.is_starting:
            t = self.big_font.render("S", True, (0, 0, 0))
            t_width = t.get_rect().width
            t_height = t.get_rect().height
            self.screen.blit(t, (x + self.node_size/2 - t_width/2, y + self.node_size/2 - t_height/2))

        elif node.is_target:
            t = self.big_font.render("T", True, (0, 0, 0))
            t_width = t.get_rect().width
            t_height = t.get_rect().height
            self.screen.blit(t, (x + self.node_size/2 - t_width/2, y + self.node_size/2 - t_height/2))

        elif self.show_numbers and (node.in_open or node.in_closed):
            f = self.big_font.render(str(node.f), True, (0, 0, 0))
            f_width = f.get_rect().width
            f_height = f.get_rect().height
            self.screen.blit(f, (x + self.node_size/2 - f_width/2, y + self.node_size/2 - f_height/2))

            h = self.small_font.render(str(node.h), True, (0, 0, 0))
            self.screen.blit(h, (x + outline_width + 1, y + outline_width + 1))

            g = self.small_font.render(str(node.g), True, (0, 0, 0))
            g_width = g.get_rect().width
            self.screen.blit(g, (x + self.node_size - g_width - outline_width - 1, y + outline_width + 1))

 
class SettingsGui():
    def __init__(self):
        self.window = tk.Tk()
        self.add_elements()
        self.window.mainloop()

    def button_event(self):
        try:
            width = int(self.e_width.get())
            height = int(self.e_height.get())
            rows = int(self.e_rows.get())
            cols = int(self.e_cols.get())
            tick_speed = int(self.e_tick_speed.get())
            if rows < 2 or cols < 2:
                raise ValueError("Must have at least 2 rows and columns.")
        except Exception as e:
            print("Could not parse input fields. Reason:")
            print(e)
            self.window.destroy()
            return

        self.window.destroy()

        gui = GUI(width, height, rows, cols, tick_speed = tick_speed)
        gui.start()


    def add_elements(self):
        tk.Label(text="Width: ").grid(row=0)
        tk.Label(text="Height: ").grid(row=1)
        tk.Label(text="Rows: ").grid(row=2)
        tk.Label(text="Columns: ").grid(row=3)
        tk.Label(text="Solve Speed (0 for instant): ").grid(row=4)

        self.e_width = tk.Entry()
        self.e_height = tk.Entry()
        self.e_rows = tk.Entry()
        self.e_cols = tk.Entry()
        self.e_tick_speed = tk.Entry()

        self.e_width.grid(row=0, column=1)
        self.e_height.grid(row=1, column=1)
        self.e_rows.grid(row=2, column=1)
        self.e_cols.grid(row=3, column=1)
        self.e_tick_speed.grid(row=4, column=1)

        self.e_width.insert(0, "700")
        self.e_height.insert(0, "700")
        self.e_rows.insert(0, "31")
        self.e_cols.insert(0, "31")
        self.e_tick_speed.insert(0, "30")

        tk.Button(text="Start", command = self.button_event).grid(row=5)

if __name__ == '__main__':
    SettingsGui()