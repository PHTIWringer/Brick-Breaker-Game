import pygame

# Ball class
class Ball:
    def __init__(self, x, y, dx, dy, radius):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius

    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def move(self):
        self.x += self.dx
        self.y += self.dy

# Power-up class
class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 6
        self.dy = 2

    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def move(self):
        self.y += self.dy