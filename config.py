from objects import Ball

# Screen setup
WIDTH, HEIGHT = 800, 1000 # Viewport 

# Colors
WHITE = (255, 255, 255) # Ball normal state
BRICK_COLOR = (170, 74, 68) # Breakable Blocks
RED = (255, 0, 0) # Ball Fire State
BLUE = (0, 0, 255) # Paddle
GRAY = (100, 100, 100) # Unbreakable blocks
BLACK = (0, 0, 0) # Background color
YELLOW = (255, 255, 0) # power up ball color

# Total block space for game)
ROWS = 30
COLS = 50

# Paddle Settings
paddle_width = 150 # pixels
paddle_speed = 15 # pixels per frame/second
paddle_height = 10 # pixels
y_coord = 30 # near bottom (30 pixels from bottom of viewport)
paddle_centering = 2 # do not change (viewport width divided by '2' to center)

# Ball settings
horizontal_postion_start = 400 # Centered
vertical_postion_start = 500 # pixels above paddle
horizontal_start_speed_per_frame = 0 # ball goes straight up at first touch
vertical_speed_per_frame = -8 # negative means upward momentum
ball_radius = 4 # size of ball * 2 for total diameter

ball = Ball(horizontal_postion_start, vertical_postion_start, horizontal_start_speed_per_frame, vertical_speed_per_frame, ball_radius)
