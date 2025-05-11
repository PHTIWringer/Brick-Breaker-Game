import pygame, os 

class Ball:
    def __init__(self, x, y, dx, dy, radius, image=None):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius
        self.image = image

    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def draw(self, screen):
        if self.image:
            # print("Drawing ball image")
            screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        else:
            # print("Drawing fallback circle")
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 6 # powerup ball radius
        self.dy = 2

    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def move(self):
        self.y += self.dy