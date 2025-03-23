import pygame
from config.const import SNAKE_IMAGES


class Snake(pygame.sprite.Sprite):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__()
        self.cell_size = cell_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"
        self.inverted_controls = False

        self.images = {key: pygame.image.load(path).convert_alpha()
                       for key, path in SNAKE_IMAGES.items()}
        for key in self.images:
            self.images[key] = pygame.transform.scale(
                self.images[key], (cell_size, cell_size))

        self.image = self.images["head_right"]
        self.rect = self.image.get_rect(topleft=self.body[0])

        self.body_sprites = pygame.sprite.Group()
        self.update_sprites()

    def update_sprites(self):
        self.body_sprites.empty()
        for i, segment in enumerate(self.body):
            segment_sprite = pygame.sprite.Sprite()
            segment_sprite.image = self.get_segment_image(i)
            segment_sprite.rect = segment_sprite.image.get_rect(
                topleft=segment)
            self.body_sprites.add(segment_sprite)

        self.image = self.get_segment_image(0)
        self.rect.topleft = self.body[0]

    def get_segment_image(self, index):
        if index == 0:
            if self.direction == "UP":
                return self.images["head_up"]
            elif self.direction == "DOWN":
                return self.images["head_down"]
            elif self.direction == "LEFT":
                return self.images["head_left"]
            elif self.direction == "RIGHT":
                return self.images["head_right"]
        elif index == len(self.body) - 1:
            tail_direction = self.get_tail_direction()
            return self.images[f"tail_{tail_direction}"]
        else:
            prev_segment = self.body[index - 1]
            next_segment = self.body[index + 1]
            return self.get_body_image(prev_segment, segment=self.body[index], next_segment=next_segment)

    def get_tail_direction(self):
        if len(self.body) < 2:
            raise ValueError(
                "Недостаточно сегментов для определения направления хвоста")

        tail = self.body[-1]
        before_tail = self.body[-2]

        if tail == before_tail:
            if self.direction == "UP":
                return "down"
            elif self.direction == "DOWN":
                return "up"
            elif self.direction == "LEFT":
                return "right"
            elif self.direction == "RIGHT":
                return "left"

        if tail[0] < before_tail[0]:
            return "left"
        elif tail[0] > before_tail[0]:
            return "right"
        elif tail[1] < before_tail[1]:
            return "up"
        elif tail[1] > before_tail[1]:
            return "down"

        raise ValueError(
            f"Не удалось определить направление хвоста: tail={tail}, before_tail={before_tail}")

    def get_body_image(self, prev_segment, segment, next_segment):
        def normalize_diff(a, b, max_val):
            diff = a - b
            if abs(diff) > max_val / 2:
                if diff > 0:
                    diff -= max_val
                else:
                    diff += max_val

            return diff

        dx_prev = normalize_diff(
            segment[0], prev_segment[0], self.screen_width)
        dy_prev = normalize_diff(
            segment[1], prev_segment[1], self.screen_height)
        dx_next = normalize_diff(
            segment[0], next_segment[0], self.screen_width)
        dy_next = normalize_diff(
            segment[1], next_segment[1], self.screen_height)

        if dx_prev == 0 and dx_next == 0:
            return self.images["body_vertical"]
        elif dy_prev == 0 and dy_next == 0:
            return self.images["body_horizontal"]
        else:
            if (dx_prev > 0 and dy_next > 0) or (dx_next > 0 and dy_prev > 0):
                return self.images["body_topleft"]
            elif (dx_prev < 0 and dy_next > 0) or (dx_next < 0 and dy_prev > 0):
                return self.images["body_topright"]
            elif (dx_prev > 0 and dy_next < 0) or (dx_next > 0 and dy_prev < 0):
                return self.images["body_bottomleft"]
            elif (dx_prev < 0 and dy_next < 0) or (dx_next < 0 and dy_prev < 0):
                return self.images["body_bottomright"]

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

        if (direction == "UP" and self.direction != "DOWN") or \
                (direction == "DOWN" and self.direction != "UP") or \
                (direction == "LEFT" and self.direction != "RIGHT") or \
                (direction == "RIGHT" and self.direction != "LEFT"):
            self.next_direction = direction

    def move(self, border_mode):
        self.direction = self.next_direction

        head_x, head_y = self.body[0]
        if self.direction == "UP":
            head_y -= self.cell_size
        elif self.direction == "DOWN":
            head_y += self.cell_size
        elif self.direction == "LEFT":
            head_x -= self.cell_size
        elif self.direction == "RIGHT":
            head_x += self.cell_size

        if border_mode:
            if head_x < 0 or head_x >= self.screen_width or head_y < 0 or head_y >= self.screen_height:
                return False
        else:
            head_x %= self.screen_width
            head_y %= self.screen_height

        self.body.insert(0, (head_x, head_y))
        self.body.pop()

        self.update_sprites()
        return True

    def grow(self):
        self.body.append(self.body[-1])
        self.update_sprites()

    def check_collision_with_food(self, food_group):
        return pygame.sprite.spritecollide(self, food_group, dokill=True)

    def check_self_collision(self):
        for segment_pos in self.body[1:]:
            if self.body[0] == segment_pos:
                return True
        return False

    def check_wall_collision(self):
        return not (0 <= self.rect.left < self.screen_width and 0 <= self.rect.top < self.screen_height)
