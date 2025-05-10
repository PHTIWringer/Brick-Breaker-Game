import game_state, pygame, config

# Handle mouse dragging brick placement
def mouse_funct_edit():
    if game_state.edit_mode and game_state.mouse_down:
        x, y = pygame.mouse.get_pos()
        bw = config.WIDTH // config.COLS
        bh = 20
        bx = (x // bw) * bw
        by = (y // bh) * bh
        rect = pygame.Rect(bx, by, bw, bh)

        if game_state.mouse_button == 1 and all(not b.colliderect(rect) for b in game_state.bricks + game_state.unbreakable_bricks):
            game_state.bricks.append(rect)
        elif game_state.mouse_button == 3 and all(not b.colliderect(rect) for b in game_state.bricks + game_state.unbreakable_bricks):
            game_state.unbreakable_bricks.append(rect)
        elif game_state.mouse_button == 2:
            game_state.bricks = [b for b in game_state.bricks if not b.colliderect(rect)]
            game_state.unbreakable_bricks = [u for u in game_state.unbreakable_bricks if not u.colliderect(rect)]
            