# colors for game (taken from chess.com for the _board_ and the pieces)
LIGHT_BG = (235, 236, 208)
DARK_BG = (119, 149, 86)

WHITE = (249, 249, 249)
BLACK = (87, 84, 82)

SILVER_CROWN = (192, 192, 192)
GOLD_CROWN = (255, 215, 0)

BLUE = (30, 144, 255)
RED = (220, 20, 60)

# measurements
WIDTH = HEIGHT = 800
ROWS = COLUMNS = 8
SQUARE_SIZE = WIDTH // COLUMNS
PIECE_RADIUS = SQUARE_SIZE // 2 - 12
SMALL_RADIUS = PIECE_RADIUS // 2

# piece codes
WHITE_PIECE = "w"
BLACK_PIECE = "b"
WHITE_QUEEN = "W"
BLACK_QUEEN = "B"
EMPTY = "_"

# directions
DOWN = 1
UP = -1
LEFT = -1
RIGHT = 1
HORIZONTAL = [LEFT, RIGHT]

# turn
HUMAN = True
COMPUTER = False

# AI
PIECE_VALUE = 30
QUEEN_VALUE = 40
CENTER_CONTROL_VALUE = 4
PIECE_DISTANCE_VALUE = 2

HASHMAP_FILE = 'datachecckers.json'
