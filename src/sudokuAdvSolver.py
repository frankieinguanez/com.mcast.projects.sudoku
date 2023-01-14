"""
Sudoku advanced solution algorithm

Author: Frankie Inguanez <br />
Date: 14/01/2023<br /><br />

A backtracking 9x9 sudoku puzzle solution algorithm with different search and guess algorithms.
"""
import sudokuPuzzleUtils as spu

def findByRow(puzzle):
    """
    Finds the next empty cell in a raster fashion, row by row.
    Arguments:
        puzzle: a 9x9 sudoku puzzle
    """
    
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] == 0:
                return (row, col)
            
    return None

def findByCol(puzzle):
    """
    Finds the next empty cell in a column order.
    Arguments:
        puzzle: a 9x9 sudoku puzzle
    """
    for col in range(0,9):
        for row in range(len(puzzle)):
            if puzzle[row][col]==0:
                return (row, col)
    
    return None

def findByBox(puzzle, mode):
    """
    Finds the next empty cell searching first by box then by row.
    Arguments:
        puzzle: a 9x9 sudoku puzzle
        mode: 3 searches for boxes sequentially, 4 searches for boxes in a zig-zag fashion, 5 searches for boxes in spiral fashion, 6 searches for boxes in a semi zig-zag fashion.
    """

    if mode==3:
        boxes=range(0,9)
    elif mode==4:
        boxes=[0,1,2,5,4,3,6,7,8]
    elif mode==5:
        boxes=[0,1,2,5,8,7,6,3,4]
    else:
        boxes=[0,1,4,3,6,7,8,5,2]

    for box in boxes:
        for row in range((box//3)*3,((box//3)*3)+3):
            for col in range((box%3)*3, ((box%3)*3)+3):
                if puzzle[row][col]==0:
                    return (row, col)

    return None

def findEmpty(puzzle, searchMode):
    """
    Finds the next empty cell in a 9x9 sudoku puzzle.
    Arguments:
        puzzle: the 9x9 sudoku puzzle.
        searchMode: defines how the puzzle is parsed: 1 by row; 2 by col; 3 by box sequentially; 4 by box in a zig-zag; 5 by box in a spiral; 6 by box in a semi-zig-zag
    """
    if searchMode==1:
        return findByRow(puzzle)
    elif searchMode==2:
        return findByCol(puzzle)
    elif searchMode>=3 and searchMode<=6:
        return findByBox(puzzle, searchMode)
    
    return None

def getGuesses(puzzle, guessMode):
    """
    Gets numbers to guess.
    Arguments:
        puzzle: the 9x9 sudoku puzzle.
        guessMode: the guessing mode. 1 for sequential, 2 for random.
    """
    import random

    if guessMode==1:
        return range(1,10)
    elif guessMode==2:
        return random.sample(range(1,10),9)

    return None

def backtracking(puzzle, searchMode, guessMode):
    """
    Solves a 9x9 sudoku puzzle using backtracking algorithm.
    Arguments:
        puzzle: the 9x9 puzzle to be solved.
        searchMode: defines how the puzzle is parsed: 1 by row; 2 by col; 3 by box sequentially; 4 by box in a zig-zag; 5 by box in a spiral; 6 by box in a semi-zig-zag
        guessMode: defines how numbers are guessed: 1 sequentially; 2 randomly
    """

    # Find the next empty cell
    find = findEmpty(puzzle, searchMode)

    # If there is no empty cell than puzzle is complete
    if not find:
        return True
    else:
        row, col = find

    # Get numbers to guess and attempt
    for guess in getGuesses(puzzle, guessMode):
        if spu.isValid(puzzle, guess, (row, col)):
            
            # Brute force guess
            puzzle[row][col] = guess

            # Attempt to solve rest of puzzle with current choice
            if backtracking(puzzle, searchMode, guessMode):
                return True

            # Invalid puzzle so backtrack
            puzzle[row][col] = 0

    return False