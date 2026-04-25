import pygame
import copy
from cell import Cell, CELL_SIZE
from sudoku_generator import SudokuGenerator

BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
THICK      = 4   
THIN       = 1   


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

        self.solution = copy.deepcopy(generator.get_board())

        
        generator.remove_cells()
        puzzle = generator.get_board()  

        self.cells = [
            [Cell(puzzle[r][c], r, c, screen) for c in range(9)]
            for r in range(9)
        ]

        self.original = copy.deepcopy(puzzle)

        self.selected_cell = None  


    def draw(self):
    
        for row in self.cells:
            for cell in row:
                cell.draw()

        board_px = 9 * CELL_SIZE
        for i in range(10):
            width = THICK if i % 3 == 0 else THIN
   
            pygame.draw.line(self.screen, BLACK,
                             (0, i * CELL_SIZE),
                             (board_px, i * CELL_SIZE), width)
      
            pygame.draw.line(self.screen, BLACK,
                             (i * CELL_SIZE, 0),
                             (i * CELL_SIZE, board_px), width)


    def select(self, row, col):
        if self.selected_cell:
            r, c = self.selected_cell
            self.cells[r][c].selected = False
        self.selected_cell = (row, col)
        self.cells[row][col].selected = True

    def click(self, x, y):
        board_px = 9 * CELL_SIZE
        if 0 <= x < board_px and 0 <= y < board_px:
            return y // CELL_SIZE, x // CELL_SIZE
        return None


    def clear(self):
        if self.selected_cell:
            r, c = self.selected_cell
            cell = self.cells[r][c]
            if not cell.locked:
                cell.set_cell_value(0)
                cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell:
            r, c = self.selected_cell
            self.cells[r][c].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            r, c = self.selected_cell
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
                self.cells[r][c].locked         = (orig != 0)

        if self.selected_cell:
            r, c = self.selected_cell
            self.cells[r][c].selected = False
            self.selected_cell = None


    def is_full(self):
        return all(self.cells[r][c].value != 0
                   for r in range(9) for c in range(9))

    def update_board(self):
        self.board = [[self.cells[r][c].value for c in range(9)]
                      for r in range(9)]

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
