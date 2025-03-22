class Snake:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = "RIGHT"
        self.inverted_controls = False

    def change_direction(self, direction):
        if self.inverted_controls:
            if direction == "UP":
                direction = "DOWN"
            elif direction == "DOWN":
                direction = "UP"
            elif direction == "LEFT":
                direction = "RIGHT"
            elif direction == "RIGHT":
                direction = "LEFT"

        # Avoiding 180 degree turns
        if (direction == "UP" and self.direction != "DOWN") or \
           (direction == "DOWN" and self.direction != "UP") or \
           (direction == "LEFT" and self.direction != "RIGHT") or \
           (direction == "RIGHT" and self.direction != "LEFT"):
            self.direction = direction

    def move(self, screen_width, screen_height):
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            head_y -= self.cell_size
        elif self.direction == "DOWN":
            head_y += self.cell_size
        elif self.direction == "LEFT":
            head_x -= self.cell_size
        elif self.direction == "RIGHT":
            head_x += self.cell_size

        head_x %= screen_width
        head_y %= screen_height

        self.body.insert(0, (head_x, head_y))
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self, position):
        return self.body[0] == position

    def check_self_collision(self):
        return self.body[0] in self.body[1:]

    def check_wall_collision(self, screen_width, screen_height):
        head_x, head_y = self.body[0]
        return head_x < 0 or head_y < 0 or head_x >= screen_width or head_y >= screen_height
