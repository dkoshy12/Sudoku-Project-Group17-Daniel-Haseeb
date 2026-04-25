import pygame
from cell import Cell, CELL_SIZE
from sudoku_generator import SudokuGenerator

BLACK = (0, 0, 0)
THICK = 4
THIN  = 1


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width      = width
        self.height     = height
        self.screen     = screen
        self.difficulty = difficulty

        removed_map = {'easy': 30, 'medium': 40, 'hard': 50}
        removed = removed_map.get(difficulty, 30)

        generator = SudokuGenerator(9, removed)
        generator.fill_values()

        full_board = generator.get_board()
        self.solution = []
        for r in range(9):
            solution_row = []
            for c in range(9):
                solution_row.append(full_board[r][c])
            self.solution.append(solution_row)

        generator.remove_cells()
        puzzle = generator.get_board()

        self.cells = []
        for r in range(9):
            cell_row = []
            for c in range(9):
                cell_row.append(Cell(puzzle[r][c], r, c, screen))
            self.cells.append(cell_row)

        self.original = []
        for r in range(9):
            original_row = []
            for c in range(9):
                original_row.append(puzzle[r][c])
            self.original.append(original_row)

        self.selected_cell = None

    def draw(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].draw()

        board_px = 9 * CELL_SIZE
        for i in range(10):
            width = THICK if i % 3 == 0 else THIN
            pygame.draw.line(self.screen, BLACK, (0, i * CELL_SIZE), (board_px, i * CELL_SIZE), width)
            pygame.draw.line(self.screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, board_px), width)

    def select(self, row, col):
        if self.selected_cell is not None:
            prev_r = self.selected_cell[0]
            prev_c = self.selected_cell[1]
            self.cells[prev_r][prev_c].selected = False
        self.selected_cell = (row, col)
        self.cells[row][col].selected = True

    def click(self, x, y):
        board_px = 9 * CELL_SIZE
        if x < 0 or x >= board_px:
            return None
        if y < 0 or y >= board_px:
            return None
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        return row, col

    def clear(self):
        if self.selected_cell is None:
            return
        r = self.selected_cell[0]
        c = self.selected_cell[1]
        cell = self.cells[r][c]
        if not cell.locked:
            cell.set_cell_value(0)
            cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell is None:
            return
        r = self.selected_cell[0]
        c = self.selected_cell[1]
        self.cells[r][c].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell is None:
            return
        r = self.selected_cell[0]
        c = self.selected_cell[1]
        cell = self.cells[r][c]
        if not cell.locked:
            cell.set_cell_value(value)
            cell.set_sketched_value(0)

    def reset_to_original(self):
        for r in range(9):
            for c in range(9):
                orig = self.original[r][c]
                self.cells[r][c].value          = orig
                self.cells[r][c].sketched_value = 0
                self.cells[r][c].locked         = orig != 0
        if self.selected_cell is not None:
            r = self.selected_cell[0]
            c = self.selected_cell[1]
            self.cells[r][c].selected = False
            self.selected_cell = None

    def is_full(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value == 0:
                    return False
        return True

    def update_board(self):
        self.board = []
        for r in range(9):
            board_row = []
            for c in range(9):
                board_row.append(self.cells[r][c].value)
            self.board.append(board_row)

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value == 0:
                    return r, c
        return None

    def check_board(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value != self.solution[r][c]:
                    return False
        return True
