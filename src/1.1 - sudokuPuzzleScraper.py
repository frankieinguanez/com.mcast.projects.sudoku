"""
# A sudoku puzzle scraper from the mypuzzle.org site.
Author: Frankie Inguanez
Date: 13/01/2023
"""

# Scraping the puzzle
def getPuzzle(code):
    import time
    import random
    import requests
    from bs4 import BeautifulSoup

    # Create header to bypass Mod_Security
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }

    puzzleUrl = "https://mypuzzle.org/app/sudoku/sudokuGet.php?iSudoku={:0.0f}"
    solutionUrl = "https://mypuzzle.org/app/sudoku/sudokuGetSolution.php?iSudoku={:0.0f}"

    # Wait for a few milliseconds so not to be blocked
    time.sleep(random.randint(0, 10)/10)

    # Get puzzle and solution
    puzzle = requests.get(puzzleUrl.format(code), headers=headers)
    solution = requests.get(solutionUrl.format(code), headers=headers)

    # Verify that response is what was expected
    if (puzzle.status_code!=200 or solution.status_code!=200):
        raise ValueError("Unexcepcted response code. Puzzle Code: {:0.0f}\nPuzzle Response Code: {:0.0f}\nSolution Response Code: {:0.0f}\n"\
            .format(code, puzzle.status_code, solution.status_code))

    if (puzzle.text.__len__()!=81 or solution.text.__len__()!=81):
        raise ValueError("Unexpected response content. Puzzle Code: {:0.0f}\nPuzzle Response: {}\nSolution Repsonse: {}\n"\
            .format(code, puzzle.text, solution.text))

    return puzzle.text, solution.text

# Save puzzle
def savePuzzle(code, puzzle, solution, fileName):
    with open(fileName, "a", encoding="utf-8") as f:
        f.write("{:0.0f}, {}, {}\n".format(code, puzzle, solution))

# Save an error should it occur
def saveError(code, error, fileName):
    try:
        with open(fileName, "a", encoding="utf-8") as f:
            f.write("Error encountered when requesting puzzle with code {:0.0f}:\n{}\n{}\n{}\n\n".format(code, type(error), error.args, error))
    except Exception as e:
        # Print error to console since we could not save to file
        print("Failed to save error to file. Exception encountered:\n{}\n{}\n{}\n\n".format(type(e), e.args, e))
        print("Original error that could not be saved to file was encountered at puzzle {:0.0f}:\n{}\n{}\n{}\n\n".format(code, type(error), error.args, error))

def scrapeSudokuPuzzles(start, finish, puzzlesFileName, errorsFileName):
    import tqdm

    # Error flag
    hasError = False

    print("Starting sudoku puzzle scraper from puzzle {:0.0f} to puzzle {:0.0f}.".format(start, finish))

    # Loop for entire range of puzzles
    for p in tqdm.tqdm(range(start, finish)):
        try:
            puzzle, solution = getPuzzle(p)
            
            if (puzzle and solution):
                savePuzzle(p, puzzle, solution, puzzlesFileName)
            else:
                raise ValueError("Received empty response for puzzle with identiication code {:0.0f}.\n".format(p))
        except Exception as inst:
            hasError = True
            saveError(p, inst, errorsFileName)

    print("Operation encountered some errors. Check {} for details or script output above.".format(errorsFileName) if hasError \
        else "Sudoku puzzles scraper completed successfully.")
    print("Sudoku puzzles saved in {}".format(puzzlesFileName))

def main():
    import argparse

    # Register arguments
    parser = argparse.ArgumentParser();
    parser.add_argument("start", help="The identification code of the first puzzle to scrape.", type=int)
    parser.add_argument("finish", help="The identification code of the puzzle to stop scraping.", type=int)
    parser.add_argument("puzzles", help="The file name where to save the puzzles.", type=str)
    parser.add_argument("errors", help="The file name where to save the errors.", type=str)

    args = parser.parse_args()

    scrapeSudokuPuzzles(args.start, args.finish, args.puzzles, args.errors)

if (__name__ == "__main__"):
    main()