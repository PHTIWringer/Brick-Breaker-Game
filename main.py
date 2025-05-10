import pygame
import sys
import random
import tkinter as tk
from tkinter import filedialog
import config
from objects import Ball, PowerUp
import game_state
import artwork

pygame.init()
tk.Tk().withdraw()  # Hide the main tkinter window

# Screen setup
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()

# Mouse tracking
mouse_down = False
mouse_button = None  # 1=left, 2=middle, 3=right

# Initialize
game_state.bricks = []
game_state.unbreakable_bricks = []
game_state.powerups = []
game_state.balls = []
game_state.reset_game()

fireball = False
font = pygame.font.SysFont(None, 36)

# Clear button
clear_button = pygame.Rect(config.WIDTH - 160, config.HEIGHT - 45, 140, 30)

# Main loop
while True:
    screen.fill((config.BLACK))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fireball = not fireball
            if event.key == pygame.K_SPACE and not game_state.game_active and not game_state.show_win:
                game_state.reset_game()
            if event.key == pygame.K_r and show_win:
                game_state.reset_game()
            if event.key == pygame.K_e:
                game_state.edit_mode = not game_state.edit_mode
            if event.key == pygame.K_s and game_state.edit_mode:
                file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
                if file_path:
                    game_state.save_layout(file_path)
            if event.key == pygame.K_l and game_state.edit_mode:
                file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
                if file_path:
                    game_state.load_layout(file_path)


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state.edit_mode and clear_button.collidepoint(event.pos):
                bricks.clear()
                unbreakable_bricks.clear()
            elif game_state.edit_mode:
                mouse_down = True
                mouse_button = event.button

        elif event.type == pygame.MOUSEBUTTONUP and game_state.edit_mode:
            mouse_down = False
            mouse_button = None

    # Handle mouse dragging brick placement
    if game_state.edit_mode and mouse_down:
        x, y = pygame.mouse.get_pos()
        bw = config.WIDTH // config.COLS
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
    if keys[pygame.K_LEFT] and artwork.paddle.left > 0:
        artwork.paddle.x -= config.paddle_speed
    if keys[pygame.K_RIGHT] and artwork.paddle.right < config.WIDTH:
        artwork.paddle.x += config.paddle_speed

    if game_state.game_active:
        for config.ball in game_state.balls[:]:
            config.ball.move()
            if config.ball.x - config.ball.radius <= 0 or config.ball.x + config.ball.radius >= config.WIDTH:
                config.ball.dx *= -1
                config.ball.x = max(ball.radius, min(config.ball.x, config.WIDTH - config.ball.radius))
            if config.ball.y - config.ball.radius <= 0:
                config.ball.dy *= -1
                config.ball.y = config.ball.radius

            if artwork.paddle.colliderect(config.ball.rect()):
                config.ball.dy = -abs(config.ball.dy)
                offset = (config.ball.x - artwork.paddle.centerx) / (artwork.paddle.width / 2)
                config.ball.dx = 5 * offset

            for brick in game_state.bricks[:]:
                if brick.colliderect(config.ball.rect()):
                    if not fireball:
                        if abs(ball.rect().bottom - brick.top) < 10 and config.ball.dy > 0:
                            config.ball.dy *= -1
                        elif abs(config.ball.rect().top - brick.bottom) < 10 and config.ball.dy < 0:
                            config.ball.dy *= -1
                        elif abs(config.ball.rect().right - brick.left) < 10 and config.ball.dx > 0:
                            config.ball.dx *= -1
                        elif abs(config.ball.rect().left - brick.right) < 10 and config.ball.dx < 0:
                            config.ball.dx *= -1
                    game_state.bricks.remove(brick)
                    if random.random() < 0.02: # % chance to spawn yellow ball
                        game_state.powerups.append(PowerUp(brick.centerx, brick.centery))
                    if random.random() < 0.02: # % chance to spawn new ball
                        game_state.balls.append(Ball(config.ball.x, config.ball.y, random.choice([-4, 8]), -8, config.ball_radius))
                    break

            for ubrick in game_state.unbreakable_bricks:
                if ubrick.colliderect(config.ball.rect()):
                    if abs(config.ball.rect().bottom - ubrick.top) < 10 and config.ball.dy > 0:
                        config.ball.dy *= -1
                        config.ball.y = ubrick.top - config.ball.radius
                    elif abs(config.ball.rect().top - ubrick.bottom) < 10 and config.ball.dy < 0:
                        config.ball.dy *= -1
                        config.ball.y = ubrick.bottom + config.ball.radius
                    elif abs(config.ball.rect().right - ubrick.left) < 10 and config.ball.dx > 0:
                        config.ball.dx *= -1
                        config.ball.x = ubrick.left - config.ball.radius
                    elif abs(config.ball.rect().left - ubrick.right) < 10 and config.ball.dx < 0:
                        config.ball.dx *= -1
                        config.ball.x = ubrick.right + config.ball.radius

            if config.ball.y - config.ball.radius > config.HEIGHT:
                game_state.balls.remove(config.ball)

        for p in game_state.powerups[:]:
            p.move()
            if artwork.paddle.colliderect(p.rect()):
                game_state.powerups.remove(p)
                if game_state.balls:
                    ref = game_state.balls[0]
                    game_state.balls.append(Ball(ref.x, ref.y, random.choice([-4, 8]), -8, config.ball_radius))
            elif p.y - p.radius > config.HEIGHT:
                game_state.powerups.remove(p)

        if not game_state.balls:
            game_state.game_active = False
        if not game_state.bricks and not show_win:
            show_win = True
            game_state.game_active = False

    # Draw game objects
    pygame.draw.rect(screen, config.BLUE, artwork.paddle)
    for ball in game_state.balls:
        pygame.draw.circle(screen, config.RED if fireball else config.WHITE, (int(ball.x), int(ball.y)), ball.radius)
    for brick in game_state.bricks:
        pygame.draw.rect(screen, config.BRICK_COLOR, brick)
        pygame.draw.rect(screen, config.BLACK, brick, 1)
    for ubrick in game_state.unbreakable_bricks:
        pygame.draw.rect(screen, config.GRAY, ubrick)
        pygame.draw.rect(screen, config.BLACK, ubrick, 1)
    for p in game_state.powerups:
        pygame.draw.circle(screen, config.YELLOW, (int(p.x), int(p.y)), p.radius)
        pygame.draw.circle(screen, config.BLACK, (int(p.x), int(p.y)), p.radius, 1)

    # Draw grid and button in edit mode
    if game_state.edit_mode:
        for x in range(0, config.WIDTH, config.WIDTH // config.COLS):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, config.HEIGHT))
        for y in range(0, config.HEIGHT, 20):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (config.WIDTH, y))
        pygame.draw.rect(screen, (80, 80, 80), clear_button)
        pygame.draw.rect(screen, config.WHITE, clear_button, 2)
        clear_text = font.render("Clear Board", True, config.WHITE)
        screen.blit(clear_text, (clear_button.x + 10, clear_button.y + 5))

    # UI text
    if not game_state.game_active and not game_state.show_win and not game_state.edit_mode:
        msg = font.render("Press SPACE to Start", True, config.WHITE)
        screen.blit(msg, (config.WIDTH // 2 - msg.get_width() // 2, config.HEIGHT // 2))

    if game_state.show_win:
        msg = font.render("You Win! Press R to Reset", True, config.WHITE)
        screen.blit(msg, (config.WIDTH // 2 - msg.get_width() // 2, config.HEIGHT // 2))

    if game_state.edit_mode:
        msg = font.render("EDIT MODE (E to exit, S to save, L to load)", True, config.WHITE)
        screen.blit(msg, (20, config.HEIGHT - 40))

    pygame.display.flip()
    clock.tick(60)
