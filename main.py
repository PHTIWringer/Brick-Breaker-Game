import pygame
import sys
import random
import json
import tkinter as tk
from tkinter import filedialog

pygame.init()
tk.Tk().withdraw()  # Hide the main tkinter window

# Screen setup
WIDTH, HEIGHT = 800, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BROWN = (170, 74, 68)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Game config
ROWS = 30
COLS = 50

# Paddle
paddle_width = 150
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 30, paddle_width, 10)
paddle_speed = 15

# Game state
game_active = False
show_win = False
edit_mode = False

# Mouse tracking
mouse_down = False
mouse_button = None  # 1=left, 2=middle, 3=right

# Ball class
class Ball:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = 4

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

# Save/Load layout
def save_layout(filename="Init_Map.json"):
    data = []
    for b in bricks:
        data.append({"x": b.x, "y": b.y, "type": "breakable"})
    for u in unbreakable_bricks:
        data.append({"x": u.x, "y": u.y, "type": "unbreakable"})
    with open(filename, "w") as f:
        json.dump(data, f)

def load_layout(filename="Init_Map.json"):
    global bricks, unbreakable_bricks
    bricks = []
    unbreakable_bricks = []
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            for b in data:
                rect = pygame.Rect(b["x"], b["y"], WIDTH // COLS, 20)
                if b["type"] == "breakable":
                    bricks.append(rect)
                else:
                    unbreakable_bricks.append(rect)
    except FileNotFoundError:
        pass

# Reset function
def reset_game():
    global balls, bricks, unbreakable_bricks, powerups, game_active, show_win, paddle
    ball_start_x = paddle.x + paddle.width // 2
    ball_start_y = paddle.y - 10
    balls = [Ball(ball_start_x, ball_start_y, 0, -8)]
    powerups = []
    load_layout("Init_Map.json")
    game_active = True
    show_win = False
    paddle.x = WIDTH // 2 - paddle.width // 2

# Initialize
bricks = []
unbreakable_bricks = []
powerups = []
balls = []
reset_game()

fireball = False
font = pygame.font.SysFont(None, 36)

# Clear button
clear_button = pygame.Rect(WIDTH - 160, HEIGHT - 45, 140, 30)

# Main loop
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fireball = not fireball
            if event.key == pygame.K_SPACE and not game_active and not show_win:
                reset_game()
            if event.key == pygame.K_r and show_win:
                reset_game()
            if event.key == pygame.K_e:
                edit_mode = not edit_mode
            if event.key == pygame.K_s and edit_mode:
                file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
                if file_path:
                    save_layout(file_path)
            if event.key == pygame.K_l and edit_mode:
                file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
                if file_path:
                    load_layout(file_path)


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if edit_mode and clear_button.collidepoint(event.pos):
                bricks.clear()
                unbreakable_bricks.clear()
            elif edit_mode:
                mouse_down = True
                mouse_button = event.button

        elif event.type == pygame.MOUSEBUTTONUP and edit_mode:
            mouse_down = False
            mouse_button = None

    # Handle mouse dragging brick placement
    if edit_mode and mouse_down:
        x, y = pygame.mouse.get_pos()
        bw = WIDTH // COLS
        bh = 20
        bx = (x // bw) * bw
        by = (y // bh) * bh
        rect = pygame.Rect(bx, by, bw, bh)

        if mouse_button == 1 and all(not b.colliderect(rect) for b in bricks + unbreakable_bricks):
            bricks.append(rect)
        elif mouse_button == 3 and all(not b.colliderect(rect) for b in bricks + unbreakable_bricks):
            unbreakable_bricks.append(rect)
        elif mouse_button == 2:
            bricks = [b for b in bricks if not b.colliderect(rect)]
            unbreakable_bricks = [u for u in unbreakable_bricks if not u.colliderect(rect)]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    if game_active:
        for ball in balls[:]:
            ball.move()
            if ball.x - ball.radius <= 0 or ball.x + ball.radius >= WIDTH:
                ball.dx *= -1
                ball.x = max(ball.radius, min(ball.x, WIDTH - ball.radius))
            if ball.y - ball.radius <= 0:
                ball.dy *= -1
                ball.y = ball.radius

            if paddle.colliderect(ball.rect()):
                ball.dy = -abs(ball.dy)
                offset = (ball.x - paddle.centerx) / (paddle.width / 2)
                ball.dx = 5 * offset

            for brick in bricks[:]:
                if brick.colliderect(ball.rect()):
                    if not fireball:
                        if abs(ball.rect().bottom - brick.top) < 10 and ball.dy > 0:
                            ball.dy *= -1
                        elif abs(ball.rect().top - brick.bottom) < 10 and ball.dy < 0:
                            ball.dy *= -1
                        elif abs(ball.rect().right - brick.left) < 10 and ball.dx > 0:
                            ball.dx *= -1
                        elif abs(ball.rect().left - brick.right) < 10 and ball.dx < 0:
                            ball.dx *= -1
                    bricks.remove(brick)
                    if random.random() < 0.02:
                        powerups.append(PowerUp(brick.centerx, brick.centery))
                    if random.random() < 0.02:
                        balls.append(Ball(ball.x, ball.y, random.choice([-4, 8]), -8))
                    break

            for ubrick in unbreakable_bricks:
                if ubrick.colliderect(ball.rect()):
                    if abs(ball.rect().bottom - ubrick.top) < 10 and ball.dy > 0:
                        ball.dy *= -1
                        ball.y = ubrick.top - ball.radius
                    elif abs(ball.rect().top - ubrick.bottom) < 10 and ball.dy < 0:
                        ball.dy *= -1
                        ball.y = ubrick.bottom + ball.radius
                    elif abs(ball.rect().right - ubrick.left) < 10 and ball.dx > 0:
                        ball.dx *= -1
                        ball.x = ubrick.left - ball.radius
                    elif abs(ball.rect().left - ubrick.right) < 10 and ball.dx < 0:
                        ball.dx *= -1
                        ball.x = ubrick.right + ball.radius

            if ball.y - ball.radius > HEIGHT:
                balls.remove(ball)

        for p in powerups[:]:
            p.move()
            if paddle.colliderect(p.rect()):
                powerups.remove(p)
                if balls:
                    ref = balls[0]
                    balls.append(Ball(ref.x, ref.y, random.choice([-4, 8]), -8))
            elif p.y - p.radius > HEIGHT:
                powerups.remove(p)

        if not balls:
            game_active = False
        if not bricks and not show_win:
            show_win = True
            game_active = False

    # Draw game objects
    pygame.draw.rect(screen, BLUE, paddle)
    for ball in balls:
        pygame.draw.circle(screen, RED if fireball else WHITE, (int(ball.x), int(ball.y)), ball.radius)
    for brick in bricks:
        pygame.draw.rect(screen, BROWN, brick)
        pygame.draw.rect(screen, BLACK, brick, 1)
    for ubrick in unbreakable_bricks:
        pygame.draw.rect(screen, GRAY, ubrick)
        pygame.draw.rect(screen, BLACK, ubrick, 1)
    for p in powerups:
        pygame.draw.circle(screen, YELLOW, (int(p.x), int(p.y)), p.radius)
        pygame.draw.circle(screen, BLACK, (int(p.x), int(p.y)), p.radius, 1)

    # Draw grid and button in edit mode
    if edit_mode:
        for x in range(0, WIDTH, WIDTH // COLS):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 20):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))
        pygame.draw.rect(screen, (80, 80, 80), clear_button)
        pygame.draw.rect(screen, WHITE, clear_button, 2)
        clear_text = font.render("Clear Board", True, WHITE)
        screen.blit(clear_text, (clear_button.x + 10, clear_button.y + 5))

    # UI text
    if not game_active and not show_win and not edit_mode:
        msg = font.render("Press SPACE to Start", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

    if show_win:
        msg = font.render("You Win! Press R to Reset", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

    if edit_mode:
        msg = font.render("EDIT MODE (E to exit, S to save, L to load)", True, WHITE)
        screen.blit(msg, (20, HEIGHT - 40))

    pygame.display.flip()
    clock.tick(60)
