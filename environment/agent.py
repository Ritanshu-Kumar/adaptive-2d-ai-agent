import math
import pygame


class Agent:
    def __init__(self, x, y, size=30):
        self.x = x
        self.y = y
        self.size = size
        self.speed = 5

    @property
    def rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        if keys[pygame.K_UP]:
            self.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.y += self.speed

    def move(self, action):
        # 0 = up, 1 = left, 2 = right, 3 = down

        if action == 0:
            self.y -= self.speed

        elif action == 1:
            self.x -= self.speed

        elif action == 2:
            self.x += self.speed

        elif action == 3:
            self.y += self.speed

    def get_sensor_distances(self, obstacles, width, height):
        max_distance = 150

        center_x = self.x + self.size / 2
        center_y = self.y + self.size / 2

        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
            "up_left": (-1, -1),
            "up_right": (1, -1),
            "down_left": (-1, 1),
            "down_right": (1, 1)
        }

        distances = {}

        for name, (dx, dy) in directions.items():
            length = math.sqrt(dx ** 2 + dy ** 2)
            dx /= length
            dy /= length

            distance = self.ray_to_boundary(
                center_x,
                center_y,
                dx,
                dy,
                width,
                height
            )

            for obstacle in obstacles:
                hit_distance = self.ray_to_rect(
                    center_x,
                    center_y,
                    dx,
                    dy,
                    obstacle.rect
                )

                if hit_distance is not None:
                    distance = min(distance, hit_distance)

            distances[name] = min(distance, max_distance)

        return distances

    def ray_to_boundary(self, x, y, dx, dy, width, height):
        distances = []

        if dx > 0:
            distances.append((width - x) / dx)
        elif dx < 0:
            distances.append((0 - x) / dx)

        if dy > 0:
            distances.append((height - y) / dy)
        elif dy < 0:
            distances.append((0 - y) / dy)

        valid_distances = [
            value for value in distances
            if value >= 0
        ]

        return min(valid_distances)

    def ray_to_rect(self, x, y, dx, dy, rect):
        if dx == 0:
            if x < rect.left or x > rect.right:
                return None

            t_min = -float("inf")
            t_max = float("inf")
        else:
            t1 = (rect.left - x) / dx
            t2 = (rect.right - x) / dx

            t_min = min(t1, t2)
            t_max = max(t1, t2)

        if dy == 0:
            if y < rect.top or y > rect.bottom:
                return None

            y_min = -float("inf")
            y_max = float("inf")
        else:
            t3 = (rect.top - y) / dy
            t4 = (rect.bottom - y) / dy

            y_min = min(t3, t4)
            y_max = max(t3, t4)

        t_enter = max(t_min, y_min)
        t_exit = min(t_max, y_max)

        if t_exit < 0 or t_enter > t_exit:
            return None

        if t_enter >= 0:
            return t_enter

        return t_exit

    def draw(self, screen, sensor_distances=None):
        pygame.draw.rect(
            screen,
            (50, 150, 255),
            self.rect
        )

        if sensor_distances is None:
            return

        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2

        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
            "up_left": (-1, -1),
            "up_right": (1, -1),
            "down_left": (-1, 1),
            "down_right": (1, 1)
        }

        for name, (dx, dy) in directions.items():
            length = math.sqrt(dx ** 2 + dy ** 2)
            dx /= length
            dy /= length

            distance = sensor_distances[name]

            end_x = center_x + dx * distance
            end_y = center_y + dy * distance

            pygame.draw.line(
                screen,
                (220, 220, 220),
                (center_x, center_y),
                (end_x, end_y),
                1
            )

            pygame.draw.circle(
                screen,
                (220, 220, 220),
                (int(end_x), int(end_y)),
                2
            )