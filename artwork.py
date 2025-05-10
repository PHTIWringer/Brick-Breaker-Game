import pygame, config

# Paddle Rendering
paddle = pygame.Rect(config.WIDTH // config.paddle_centering - config.paddle_width // config.paddle_centering, config.HEIGHT - config.y_coord, config.paddle_width, config.paddle_height)