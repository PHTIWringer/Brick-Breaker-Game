import pygame, sys, random, config, game_state, artwork, edit
import tkinter as tk
from tkinter import filedialog
from objects import Ball, PowerUp, Player

pygame.init()
tk.Tk().withdraw()  # Hide the main tkinter window

# Select player before starting
print("Available players:", list(game_state.players.keys()))
name = input("Enter player name: ").strip()

if name in game_state.players:
    active_player = game_state.players[name]
    print(f"Active player: {active_player.name}")
else:
    from objects import Player
    active_player = Player(name)
    game_state.players[name] = active_player
    print(f"New profile created: {active_player.name}")

# Initialize
game_state.bricks = []
game_state.unbreakable_bricks = []
game_state.powerups = []
game_state.balls = []
game_state.reset_game()
font = pygame.font.SysFont(None, 36)
last_minute_time = pygame.time.get_ticks()
last_score = -1
xp_awarded = False

# Main loop
while True:
    config.screen.fill((config.BLACK))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            xp_earned = active_player.convert_score_to_xp()
            for player in game_state.players.values():
                active_player.save()
            print(f"\nExiting... XP earned: {xp_earned:.1f} | Total XP: {active_player.total_xp:.1f}")
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                config.fireball = not config.fireball
            if event.key == pygame.K_SPACE and not game_state.game_active and not game_state.show_win:
                game_state.reset_game()
                xp_awarded = False
            if event.key == pygame.K_r and show_win:
                xp_earned = active_player.convert_score_to_xp()
                print(f"\nGame Over. XP earned: {xp_earned:.1f} | Total XP: {active_player.total_xp:.1f}")
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                game_state.edit_mode = not game_state.edit_mode           
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state.edit_mode and config.clear_button.collidepoint(event.pos):
                game_state.bricks.clear()
                game_state.unbreakable_bricks.clear()
            elif game_state.edit_mode:
                game_state.mouse_down = True
                game_state.mouse_button = event.button

        elif event.type == pygame.MOUSEBUTTONUP and game_state.edit_mode:
            game_state.mouse_down = False
            game_state.mouse_button = None

        if game_state.edit_mode:
            edit.mouse_funct_edit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and artwork.paddle.left > 0:
        artwork.paddle.x -= config.paddle_speed
    if keys[pygame.K_RIGHT] and artwork.paddle.right < config.WIDTH:
        artwork.paddle.x += config.paddle_speed

    if game_state.game_active:
        current_time = pygame.time.get_ticks()
        if current_time - last_minute_time >= 60000:
            active_player.add_score(100)
            last_minute_time = current_time

        for ball in game_state.balls[:]:
            ball.move()
            if ball.x - ball.radius <= 0 or ball.x + ball.radius >= config.WIDTH:
                ball.dx *= -1
                ball.x = max(ball.radius, min(ball.x, config.WIDTH - ball.radius))
            if ball.y - ball.radius <= 0:
                ball.dy *= -1
                ball.y = ball.radius

            if artwork.paddle.colliderect(ball.rect()):
                ball.dy = -abs(ball.dy)
                offset = (ball.x - artwork.paddle.centerx) / (artwork.paddle.width / 2)
                ball.dx = 5 * offset

            for brick in game_state.bricks[:]:
                if brick.colliderect(ball.rect()):
                    if not config.fireball:
                        if abs(ball.rect().bottom - brick.top) < 10 and ball.dy > 0:
                            ball.dy *= -1
                        elif abs(ball.rect().top - brick.bottom) < 10 and ball.dy < 0:
                            ball.dy *= -1
                        elif abs(ball.rect().right - brick.left) < 10 and ball.dx > 0:
                            ball.dx *= -1
                        elif abs(ball.rect().left - brick.right) < 10 and ball.dx < 0:
                            ball.dx *= -1
                    game_state.bricks.remove(brick)
                    active_player.add_score(1)

                    if random.random() < 0.02: # % chance to spawn yellow ball
                        game_state.powerups.append(PowerUp(brick.centerx, brick.centery))
                    if random.random() < 0.02: # % chance to spawn new ball
                        game_state.balls.append(Ball(ball.x, ball.y, random.choice([-4, 8]), -8, config.ball_radius, image=config.shared_ball_image))
                    break

            for ubrick in game_state.unbreakable_bricks:
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
                        ball.x = ubrick.right + config.ball.radius

            if ball.y - ball.radius > config.HEIGHT:
                game_state.balls.remove(ball)

        for p in game_state.powerups[:]:
            p.move()
            if artwork.paddle.colliderect(p.rect()):
                game_state.powerups.remove(p)
                if game_state.balls:
                    ref = game_state.balls[0]
                    game_state.balls.append(Ball(ref.x, ref.y, random.choice([-4, 8]), -8, config.ball_radius, image=config.shared_ball_image))
            elif p.y - p.radius > config.HEIGHT:
                game_state.powerups.remove(p)

        if not game_state.balls:
            game_state.game_active = False
        if not game_state.bricks and not show_win:
           # xp_earned = game_state.player1.convert_score_to_xp()
            #print(f"\n🏆 You won! XP earned: {xp_earned:.1f} | Total XP: {game_state.player1.total_xp:.1f}")
            show_win = True
            game_state.game_active = False

    # Draw game objects
    pygame.draw.rect(config.screen, config.BLUE, artwork.paddle)
    for ball in game_state.balls:
        ball.draw(config.screen)
    for brick in game_state.bricks:
        pygame.draw.rect(config.screen, config.BRICK_COLOR, brick)
        pygame.draw.rect(config.screen, config.BLACK, brick, 1)
    for ubrick in game_state.unbreakable_bricks:
        pygame.draw.rect(config.screen, config.GRAY, ubrick)
        pygame.draw.rect(config.screen, config.BLACK, ubrick, 1)
    for p in game_state.powerups:
        pygame.draw.circle(config.screen, config.YELLOW, (int(p.x), int(p.y)), p.radius)
        pygame.draw.circle(config.screen, config.BLACK, (int(p.x), int(p.y)), p.radius, 1)

    # Draw grid and button in edit mode
    if game_state.edit_mode:
        for x in range(0, config.WIDTH, config.WIDTH // config.COLS):
            pygame.draw.line(config.screen, (40, 40, 40), (x, 0), (x, config.HEIGHT))
        for y in range(0, config.HEIGHT, 20):
            pygame.draw.line(config.screen, (40, 40, 40), (0, y), (config.WIDTH, y))
        pygame.draw.rect(config.screen, (80, 80, 80), config.clear_button)
        pygame.draw.rect(config.screen, config.WHITE, config.clear_button, 2)
        clear_text = font.render("Clear Board", True, config.WHITE)
        config.screen.blit(clear_text, (config.clear_button.x + 10, config.clear_button.y + 5))

    # UI text
    if not game_state.game_active and not game_state.show_win and not game_state.edit_mode:
        msg = font.render("Press SPACE to Start", True, config.WHITE)
        config.screen.blit(msg, (config.WIDTH // 2 - msg.get_width() // 2, config.HEIGHT // 2))
        
        if not xp_awarded:
            xp_earned = active_player.convert_score_to_xp()
            print(f"\nGame ended. XP earned: {xp_earned:.1f} | Total XP: {active_player.total_xp:.1f}")
            xp_awarded = True

    if game_state.show_win:
        msg = font.render("You Win! Press R to Reset", True, config.WHITE)
        config.screen.blit(msg, (config.WIDTH // 2 - msg.get_width() // 2, config.HEIGHT // 2))

    if game_state.edit_mode:
        msg = font.render("EDIT MODE (E to exit, S to save, L to load)", True, config.WHITE)
        config.screen.blit(msg, (20, config.HEIGHT - 40))

    if active_player != last_score:
        print(f"Score: {active_player.score}", end='\r')
        last_score = active_player.score

    pygame.display.flip()
    config.clock.tick(60)
