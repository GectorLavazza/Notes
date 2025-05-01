FPS = 60

WIDTH, HEIGHT = 1280, 720

screen_width, screen_height = WIDTH, HEIGHT
screen_size = screen_width, screen_height

CENTER = screen_width // 2, screen_height // 2

EDITOR_FONT_SIZE = 16

BLACK = (52, 52, 52)
WHITE = (243, 243, 243)
DARKEST_BLACK = (35, 35, 35)

TURQUOISE = (0, 255, 255)

from os import path, listdir

PATH = path.dirname(__file__) + '/'
print(PATH)

FILES = [f[:-3] for f in listdir(PATH) if f.endswith('.py')]
print(FILES)

PARENTHESES = {
    '(': '()',
    '{': '{}',
    '[': '[]',
}

CLOSING_PARENTHESES = {
    ')': '()',
    '}': '{}',
    ']': '[]'
}
