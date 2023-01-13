"""
Data cleaning and Util functions

Author: Frankie Inguanez <br />
Date: 13/01/2023<br /><br />

A series of utility functions to clean and check a sudoku puzzle.
"""

# Get number of lines in a file
def getFileLineCount(fileName):
    import mmap

    lines = 0
    with open(fileName, "r+", encoding="utf-8") as f:
        bf = mmap.mmap(f.fileno(), 0)

        while bf.readline():
            lines += 1

    return lines

# Saves an error
def saveError(error, errorsFileName):
    try:
        with open(errorsFileName, "a", encoding="utf-8") as ef:
            ef.write("Encountered error:\n{}\n{}\n{}\n\n".format(type(error), error.args, error))
    except Exception as e:
        # Failed to save error to file
        print("Failed to save original error to file due to:\n{}\n{}\n{}\n\n".format(type(e), e.args, e))
        print("Original error:\n{}\n{}\n{}\n\n".format(type(error), error.args, error))

# Convert a string to a 2D 9x9 array.
def to2DArray(n):
    return [list(map(int, n[i:i+9])) for i in range(0, 81, 9)]

# Get column values
def getColValues(puzzle, col):
    lst = []
    for row in puzzle:
        lst.append(row[col])

    return lst;

# Get box values. Boxes are 3x3 sub-grids enumerates from top left in a raster fashion
# 0, 1, 2
# 3, 4, 5
# 6, 7, 8
def getBoxValues(puzzle, box):
    return [puzzle[x][y] for x in range((box//3)*3,((box//3)*3)+3) for y in range((box%3)*3, ((box%3)*3)+3)]

# Check if a list of digits contain all values from 1 to 9
def checkList(lst):
    return set(lst) == set(range(1,10))

# Check if a puzzle has been solved
def isSolved(puzzle):
    # Check rows
    for row in puzzle:
        if not checkList(row):
            return False

    # Check columns
    for i in range(0,9):
        if not checkList(getColValues(puzzle, i)):
            return False;

    # Check box
    for i in range(0,9):
        if not checkList(getBoxValues(puzzle, i)):
            return False;

    return True

# Checks if a number can be added to a specific position
def isValid(puzzle, num, pos):
    # Check the row
    for i in range(len(puzzle[0])):
        if puzzle[pos[0]][i]==num and pos[1] != i:
            return False

    # Check the column
    for i in range(len(puzzle[1])):
        if puzzle[i][pos[1]]==num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if puzzle[i][j] == num and (i,j) != pos:
                return False

    return True
