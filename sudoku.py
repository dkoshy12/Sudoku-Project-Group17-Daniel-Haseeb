import sys
import pygame
from cell import CELL_SIZE
from board import Board

BOARD_PX   = 9 * CELL_SIZE
BTN_HEIGHT = 50
WIN_W      = BOARD_PX
WIN_H      = BOARD_PX + BTN_HEIGHT + 20

FPS = 60


DARK_BLUE    = (30,  60, 120)
ACCENT       = (70, 130, 180)
GRAY         = (160, 160, 160)
GREEN        = (50,  160,  50)
RED          = (200,  50,  50)


def make_button(text, rect, font, screen, color, text_color=(255,255,255)):
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = font.render(text, True, text_color)
    lr    = label.get_rect(center=rect.center)
    screen.blit(label, lr)


def draw_centered_text(screen, text, y, font, color):
    label = font.render(text, True, color)
    rect  = label.get_rect(centerx=WIN_W // 2, top=y)
    screen.blit(label, rect)


def start_screen(screen, clock):
    title_font = pygame.font.SysFont("Arial", 48, bold=True)
    sub_font   = pygame.font.SysFont("Arial", 22)
    btn_font   = pygame.font.SysFont("Arial", 26, bold=True)

    btn_w   = 180
    btn_h   = 54
    spacing = 20
    total_w = 3 * btn_w + 2 * spacing
    start_x = (WIN_W - total_w) // 2
    btn_y   = WIN_H // 2 + 30

    easy_rect   = pygame.Rect(start_x,                      btn_y, btn_w, btn_h)
    medium_rect = pygame.Rect(start_x + btn_w + spacing,    btn_y, btn_w, btn_h)
    hard_rect   = pygame.Rect(start_x + 2 * (btn_w + spacing), btn_y, btn_w, btn_h)

    easy_color   = (60,  160,  60)
    medium_color = (200, 140,  40)
    hard_color   = (200,  50,  50)

    while True:
        screen.fill((255,255,255))
        draw_centered_text(screen, "SUDOKU", WIN_H // 2 - 110, title_font, DARK_BLUE)

        sub = sub_font.render("Select a difficulty to begin", True, GRAY)
        screen.blit(sub, sub.get_rect(centerx=WIN_W // 2, top=WIN_H // 2 - 45))

        make_button("Easy",   easy_rect,   btn_font, screen, (0,0,0))
        make_button("Medium", medium_rect, btn_font, screen, medium_color)
        make_button("Hard",   hard_rect,   btn_font, screen, hard_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if easy_rect.collidepoint(event.pos):
                    return 'easy'
                if medium_rect.collidepoint(event.pos):
                    return 'medium'
                if hard_rect.collidepoint(event.pos):
                    return 'hard'

        pygame.display.flip()
        clock.tick(FPS)


def end_screen(screen, clock, won):
    title_font = pygame.font.SysFont("Arial", 52, bold=True)
    btn_font   = pygame.font.SysFont("Arial", 26, bold=True)
    sub_font   = pygame.font.SysFont("Arial", 22)

    if won:
        bg    = (220, 255, 220)
        color = GREEN
        msg   = "You Win!"
        sub   = "Congratulations, the puzzle is solved!"
    else:
        bg    = (255, 220, 220)
        color = RED
        msg   = "Game Over"
        sub   = "The board isn't quite right."

    restart_rect = pygame.Rect(WIN_W // 2 - 210, WIN_H // 2 + 40, 180, 52)
    exit_rect    = pygame.Rect(WIN_W // 2 + 30,  WIN_H // 2 + 40, 180, 52)

    while True:
        screen.fill(bg)
        draw_centered_text(screen, msg, WIN_H // 2 - 100, title_font, color)

        sl = sub_font.render(sub, True, (0, 0, 0))
        screen.blit(sl, sl.get_rect(centerx=WIN_W // 2, top=WIN_H // 2 - 30))

        make_button("Play Again", restart_rect, btn_font, screen, ACCENT)
        make_button("Exit",       exit_rect,    btn_font, screen, (160, 60, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(event.pos):
                    return 'restart'
                if exit_rect.collidepoint(event.pos):
                    return 'exit'

        pygame.display.flip()
        clock.tick(FPS)


def game_screen(screen, clock, difficulty):
    btn_font = pygame.font.SysFont("Arial", 22, bold=True)

    board = Board(BOARD_PX, BOARD_PX, screen, difficulty)

    btn_w = 130
    btn_h = 42
    btn_y = BOARD_PX + 12
    gap   = (WIN_W - 3 * btn_w) // 4

    reset_rect   = pygame.Rect(gap,               btn_y, btn_w, btn_h)
    restart_rect = pygame.Rect(gap * 2 + btn_w,   btn_y, btn_w, btn_h)
    exit_rect    = pygame.Rect(gap * 3 + btn_w * 2, btn_y, btn_w, btn_h)

    while True:
        screen.fill((255, 255, 255))
        board.draw()

        make_button("Reset",   reset_rect,   btn_font, screen, (80,  130, 200))
        make_button("Restart", restart_rect, btn_font, screen, (200, 140,  40))
        make_button("Exit",    exit_rect,    btn_font, screen, (200,  60,  60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx = event.pos[0]
                my = event.pos[1]

                if reset_rect.collidepoint(mx, my):
                    board.reset_to_original()
                elif restart_rect.collidepoint(mx, my):
                    return 'restart'
                elif exit_rect.collidepoint(mx, my):
                    return 'exit'
                else:
                    cell_pos = board.click(mx, my)
                    if cell_pos is not None:
                        board.select(cell_pos[0], cell_pos[1])

            if event.type == pygame.KEYDOWN and board.selected_cell is not None:
                r = board.selected_cell[0]
                c = board.selected_cell[1]

                if event.key == pygame.K_UP and r > 0:
                    board.select(r - 1, c)
                elif event.key == pygame.K_DOWN and r < 8:
                    board.select(r + 1, c)
                elif event.key == pygame.K_LEFT and c > 0:
                    board.select(r, c - 1)
                elif event.key == pygame.K_RIGHT and c < 8:
                    board.select(r, c + 1)
                elif event.unicode.isdigit() and event.unicode != '0':
                    board.sketch(int(event.unicode))
                elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                    board.clear()
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    cell = board.cells[r][c]
                    if cell.sketched_value != 0:
                        board.place_number(cell.sketched_value)

        if board.is_full():
            pygame.display.flip()
            result = end_screen(screen, clock, board.check_board())
            return result

        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Sudoku")
    clock  = pygame.time.Clock()

    while True:
        difficulty = start_screen(screen, clock)
        result     = game_screen(screen, clock, difficulty)
        if result == 'exit':
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
