import os

# ========== Screen Settings ==========
WIDTH = 800
HEIGHT = 600
FPS = 60

# ========== Bird Settings ==========
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
JUMP_STRENGTH = -10
GRAVITY = 0.3

# ========== Pipe Settings ==========
PIPE_WIDTH = 80
PIPE_SPEED = 3

# Pipe Gap Range for Randomization
MIN_PIPE_GAP = 150
MAX_PIPE_GAP = 250

# ========== Asset Directory ==========
ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# ========== Fallback Colors (in case assets are missing) ==========
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)