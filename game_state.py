import json, pygame, config, artwork
from objects import Ball

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
                rect = pygame.Rect(b["x"], b["y"], config.WIDTH // config.COLS, 20)
                if b["type"] == "breakable":
                    bricks.append(rect)
                else:
                    unbreakable_bricks.append(rect)
    except FileNotFoundError:
        pass

def reset_game():
    global balls, bricks, unbreakable_bricks, powerups, game_active, show_win, artwork
    ball_start_x = artwork.paddle.x + config.paddle_width // 2
    ball_start_y = artwork.paddle.y - 10
    balls = [Ball(ball_start_x, ball_start_y, 0, -8, config.ball_radius)]
    powerups = []
    load_layout("Init_Map.json")
    game_active = True
    show_win = False
    artwork.paddle.x = config.WIDTH // 2 - config.paddle_width // 2

# Game state
game_active = False
show_win = False
edit_mode = False

# Mouse tracking
mouse_down = False
mouse_button = None  # 1=left, 2=middle, 3=right