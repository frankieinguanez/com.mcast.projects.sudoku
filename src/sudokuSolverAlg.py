"""
Sudoku solver algorithms

Author: Frankie Inguanez
Date: 15/01/2023

A series of solution algorithms for sudoku puzzles.
"""

import sudokuSearchAlg as ssa
import sudokuGuessAlg as sga
import sudokuPuzzleUtils as spu

def backtracking(board, stats: spu.SudokuStats, searchMode: int, guessMode: int):
    """
    Solves a 9x9 sudoku puzzle using backtracking algorithm.
    Arguments:
        board: the 9x9 puzzle to be solved.
        stats: The statistics object to record algorithm.
        searchMode: defines how the puzzle is parsed to find an empty cell.
        guessMode: defines how numbers are guessed: 1 sequentially; 2 randomly
    """
    # Find the next empty cell
    find = ssa.findEmpty(board, searchMode)

    # If there is no empty cell than puzzle is complete
    if not find:
        stats.registerEndTime()
        return True
    else:
        row, col = find

    # Get numbers to guess and attempt
    for guess in sga.getGuesses(board, guessMode):
        if spu.isValid(board, guess, (row, col)):

            # Brute force guess
            stats.incrementGuesses()
            board[row][col] = guess

            # Attempt to solve rest of puzzle with current choice
            if backtracking(board, stats, searchMode, guessMode):
                return True

            # Invalid puzzle so backtrack
            stats.incrementBacktracks()
            board[row][col] = 0

    return False
