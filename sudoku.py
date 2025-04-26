from typing import Callable

import numpy as np
from pycsp3 import *
from myCSP.mycsp import *
from board import Board
from refresher import *

class Layout:
    """
    Represents a Sudoku puzzle layout and provides methods to solve it using different CSP algorithms.

    This class reads a Sudoku layout from a file, initializes the puzzle grid, and provides solving functions
    using both PyCSP and a our csp solver, mycsp (YAY!!!). The solutions enforce constraints such as row, 
    column, and 3x3 block uniqueness, and allow for various heuristic optimizations.

    Attributes:
        clues (list[list[int]]): A 9x9 grid representing the initial Sudoku puzzle state.
    """
    def __init__(self, path):
        """Initializes the Sudoku layout by reading a file and parsing the puzzle grid."""
        with open(path, "r") as file:
            text = file.read()
            words = text.split()
            numbers = []
            for w in words:
                if w == "_":
                    numbers.append(0)
                else:
                    numbers.append(int(w))

        self.clues = np.reshape(numbers, (9, 9)).tolist()

    def get_clues(self):
        """Returns the initial Sudoku clues."""
        return self.clues









    def pycsp_solve(self, board: Board) -> bool:
        from pycsp3 import clear, VarArray, satisfy, AllDifferent, solve, values

        clear()
        # there was some problem in reading the first popping uo table to read its values. I added this to
        # manually make sure it gets prefixed values right
        self.clues = board.layout_board
        grid_vars = VarArray(size=[9, 9], dom=range(1, 10))
        predefined = self.clues

        for row_idx in range(9):
            for col_idx in range(9):
                num = predefined[row_idx][col_idx]
                if num > 0:
                    satisfy(grid_vars[row_idx][col_idx] == num)

        for row_cells in grid_vars:
            satisfy(AllDifferent(row_cells))

        for col_idx in range(9):
            satisfy(AllDifferent([grid_vars[row][col_idx] for row in range(9)]))

        for r_base in (0, 3, 6):
            for c_base in (0, 3, 6):
                region = [grid_vars[r][c] for r in range(r_base, r_base + 3)
                          for c in range(c_base, c_base + 3)]
                satisfy(AllDifferent(region))

        if solve():
            filled = values(grid_vars)
            board.answer_board = [list(filled[r]) for r in range(9)]
            return True

        return False

    def mycsp_solve(self,
                    board: Board,
                    do_unary_check: bool,
                    do_arc_consistency: bool,
                    use_mrv: bool,
                    use_lcv: bool,
                    show_steps: bool,
                    update_ui: Callable[[], None],
                    check_terminate: Callable[[], bool]) -> bool:
        import time
        start_time = time.process_time()

        my_clear()
        self.clues = board.layout_board

        sudoku_cells = myVarArray("GridVars", (9, 9), set(range(1, 10)))

        for r_idx, row in enumerate(self.clues):
            for c_idx, val in enumerate(row):
                if val > 0:
                    unary_condition = myUnaryConstraint(
                        sudoku_cells[r_idx][c_idx], val, lambda x, y: x == y
                    )
                    constraint_list.append(unary_condition)

        for row_vars in sudoku_cells:
            my_satisfy(myAllDifferent(row_vars))

        for c in range(9):
            my_satisfy(myAllDifferent([sudoku_cells[r][c] for r in range(9)]))

        for r_base in range(0, 9, 3):
            for c_base in range(0, 9, 3):
                region = [sudoku_cells[r][c] for r in range(r_base, r_base + 3)
                          for c in range(c_base, c_base + 3)]
                my_satisfy(myAllDifferent(region))

        ui_helper = Refresher(sudoku_cells, board, show_steps, update_ui, check_terminate)

        success = my_solve(do_unary_check, do_arc_consistency, use_mrv, use_lcv, ui_helper)

        if success:
            board.answer_board = [[sudoku_cells[r][c].value for c in range(9)] for r in range(9)]

        elapsed = time.process_time() - start_time
        print(elapsed * 10, "seconds")

        return success

    def solve(self,
              algorithm: str, 
              do_unary_check: bool, 
              do_arc_consistency: bool, 
              do_mrv: bool,
              do_lcv: bool,
              real_time: bool, 
              board: Board,
              refresh: Callable[[],bool],
              get_stop_event: Callable[[], bool]):
        #for checking the name of the algorithm
        #print("DEBUG — selected algorithm:", algorithm)
        """Solves the Sudoku puzzle using the selected CSP algorithm."""

        if algorithm == 'pycsp':
            return self.pycsp_solve(board)
        else:
            return self.mycsp_solve(board, do_unary_check, 
                                    do_arc_consistency, 
                                    do_mrv, 
                                    do_lcv, 
                                    real_time, 
                                    refresh,
                                    get_stop_event)