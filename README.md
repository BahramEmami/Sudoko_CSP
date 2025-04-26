Sudoku Solver using CSP Techniques

This project is a Sudoku puzzle solver developed using Constraint Satisfaction Problem (CSP) techniques. 
It was created as part of a project for the Fundamentals of Artificial Intelligence course at Amirkabir University of Technology (AUT), Computer Engineering Department.

Project Overview

The solver offers two main modes:
- pycsp mode: Solves Sudoku puzzles using the external pycsp3 library.
- mycsp mode: A custom CSP solver written from scratch without external solving engines.

Both solvers model Sudoku as a CSP with:
- Variables (X): Each cell in the 9×9 Sudoku grid.
- Domains (D): Possible values {1, ..., 9}.
- Constraints (C): Standard Sudoku rules (row, column, and block uniqueness).

Features

- Full GUI built with Pygame and Pygame-GUI.
- Real-time solving visualization (optional).
- Heuristic options:
    - Unary Consistency
    - Arc Consistency (AC-3)
    - MRV (Minimum Remaining Values)
    - LCV (Least Constraining Value)
- Load custom Sudoku layouts.
- Solves puzzles from easy to evil difficulty.

Technologies Used

- Python 3.x
- Pygame
- Pygame-GUI
- pycsp3

Project Structure

├── main.py
├── sudoku.py
├── board.py
├── refresher.py
├── exceptions.py
├── layouts/
│   └── *.sudoku
├── myCSP/
│   ├── mycsp.py
│   ├── myVariable.py
│   ├── myVarArray.py
│   ├── myConstraint.py
│   ├── AllDifferent.py
└── theme.json

How to Run

1. Clone the repository:
   git clone https://github.com/yourusername/sudoku-csp-solver.git
   cd sudoku-csp-solver

2. Install dependencies:
   pip install pygame pygame_gui pycsp3

3. Launch the application:
   python main.py

4. Load a Sudoku puzzle, choose a solving method (pycsp or mycsp), set your heuristics, and click Solve!

Notes

- Solving hard puzzles like Evil.sudoku without enabling heuristics can be very slow using mycsp.
- Enabling MRV, LCV, and Arc Consistency is highly recommended for better performance.

Project Information

Developed for:

- Course: Fundamentals of Artificial Intelligence
- University: Amirkabir University of Technology (AUT)
- Department: Computer Engineering

License

This project is for educational purposes and internal university usage only. 
For external use or modification, please mention the original authors.

Short GitHub Description

Sudoku Solver using CSP techniques (AC-3, Backtracking, MRV, LCV). Project for Fundamentals of AI - Amirkabir University (AUT), Computer Engineering.

