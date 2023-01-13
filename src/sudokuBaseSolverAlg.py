"""
Sudoku base solution algorithm

Author: Frankie Inguanez <br />
Date: 13/01/2023<br /><br />

A basic brute force, solution algorithm with backtracking.
"""
from sudokuPuzzleUtils import *

# Finds the next empty cell in a raster fashion.
def findRaster(puzzle):
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] == 0:
                return (row, col)
            
    return None

# Solves a sudoku 9x9 puzzle in a raster pattern using sequential brute force guessing.
def solveRaster(puzzle):
    
    find = findRaster(puzzle)

    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if isValid(puzzle, i, (row, col)):
            puzzle[row][col] = i

            if solveRaster(puzzle):
                return True

            puzzle[row][col] = 0

    return False

def solvePuzzles(puzzlesFileName, statsFileName, errorsFileName, limit):
    import tqdm

    if not limit:
        limit = getFileLineCount(puzzlesFileName)

    i = 0
    hasError = False
    try:
        print("Starting sudoku base solver.")
        
        with open(statsFileName, "w", encoding="utf-8") as sf:
            with open(puzzlesFileName, "r", encoding="utf-8") as pf:
                for line in tqdm.tqdm(pf, total=limit):
                    # Parse the content
                    data = line.split(',')
                    p = data[1].strip()

                    puzzle = to2DArray(p)

                    if not solveRaster(puzzle):
                        sf.write("Could not solve puzzle {:0.0f}".format(data[0]))

                    i+=1

                    if (i>limit):
                        break

    except Exception as e:
        hasError = True
        saveError(e, errorsFileName)

    print("Operation encountered some errors. Check {} for details or script output above.".format(errorsFileName) \
        if hasError else "Sudoku puzzles solved completed successfully.")
    print("Sudoku solver statistics saved in {}".format(statsFileName))