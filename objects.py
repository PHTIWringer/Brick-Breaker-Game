import pygame, os, json 

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

class Player:
    def __init__(self, name, total_xp=0.0, points=0):
        self.name = name
        self.score = 0
        self.total_xp = total_xp
        self.points = points

    def add_score(self, amount):
        self.score += amount

    def convert_score_to_xp(self, rate=0.1):
        xp_gained = self.score * rate
        self.total_xp += xp_gained
        self.score = 0
        return xp_gained

    def save(self):
        data = {
            "name": self.name,
            "total_xp": self.total_xp,
            "points": self.points
        }
        with open(f"{self.name}_save.json", "w") as f:
            json.dump(data, f)

    @staticmethod
    def load(name):
        filename = f"{name}_save.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
            return Player(data["name"], data["total_xp"], data["points"])
        else:
            return Player(name)
    