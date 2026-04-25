import pygame

WHITE        = (255, 255, 255)
BLACK        = (0,   0,   0)
LIGHT_BLUE   = (173, 216, 230)
DARK_GRAY    = (80,  80,  80)
SKETCH_COLOR = (100, 100, 200)

CELL_SIZE = 60


class Cell:
    def __init__(self, value, row, col, screen):
        self.value          = value
        self.sketched_value = 0
        self.row            = row
        self.col            = col
        self.screen         = screen
        self.selected       = False
        self.locked         = value != 0

    def set_cell_value(self, value):
        if not self.locked:
            self.value = value

    def set_sketched_value(self, value):
        if not self.locked:
            self.sketched_value = value

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.selected:
            pygame.draw.rect(self.screen, LIGHT_BLUE, (x, y, CELL_SIZE, CELL_SIZE))

        if self.value != 0:
            font  = pygame.font.SysFont("Arial", 36, bold=self.locked)
            color = BLACK if self.locked else DARK_GRAY
            text  = font.render(str(self.value), True, color)
            rect  = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            self.screen.blit(text, rect)
        elif self.sketched_value != 0:
            font = pygame.font.SysFont("Arial", 18)
            text = font.render(str(self.sketched_value), True, SKETCH_COLOR)
            self.screen.blit(text, (x + 5, y + 5))
