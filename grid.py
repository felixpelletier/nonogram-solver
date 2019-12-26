
class Grid:

    def __init__(self, width, height):
        self.debug_print = False
        self.width = width
        self.height = height
        self.grid = Grid.make_grid(width, height)

    @staticmethod
    def make_grid(width, height):
        return [[0] * height for i in range(width)]

    @staticmethod
    def from_problem(problem):
        return Grid(len(problem[0]), len(problem[1]))

    def apply_row(self, y, values):
        for x in range(len(self.grid)):
            self.grid[x][y] = values[x]

    def apply_column(self, x, values):
        for y in range(len(self.grid[x])):
            self.grid[x][y] = values[y]

    def get_row(self, y):
        return tuple(self.grid[x][y] for x in range(len(self.grid)))

    def get_column(self, x):
        return tuple(self.grid[x])

    def is_solved(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y] == 0:
                    return False

        return True

    def __repr__(self):
        result = ""
        for y in range(len(self.grid[0])):
            result += " ".join(str(self.grid_value_to_char(self.grid[x][y])) for x in range(len(self.grid)))
            result += "\n"

        return result

    def grid_value_to_char(self, value):
        if value == 1:
            return "#"
        elif value == -1 and self.debug_print:
            return "x"

        return "·"

