"""
Data exploration

Author: Frankie Inguanez <br />
Date: 13/01/2023 <br /> <br />

An evaluator of sudoku puzzles
"""

# Saves an error
def saveError(error, errorsFileName):
    try:
        with open(errorsFileName, "a", encoding="utf-8") as ef:
            ef.write("Encountered error:\n{}\n{}\n{}\n\n".format(type(error), error.args, error))
    except Exception as e:
        # Failed to save error to file
        print("Failed to save original error to file due to:\n{}\n{}\n{}\n\n".format(type(e), e.args, e))
        print("Original error:\n{}\n{}\n{}\n\n".format(type(error), error.args, error))

# Get number of lines in a file
def getFileLineCount(fileName):
    import mmap

    lines = 0
    with open(fileName, "r+", encoding="utf-8") as f:
        bf = mmap.mmap(f.fileno(), 0)

        while bf.readline():
            lines += 1

    return lines

# Save stats
def saveStats(stats, statsFileName):
    with open(statsFileName, "w", encoding="utf-8") as sf:
        for i in range(0, 81):
            if stats[i] ==0:
                continue

            sf.write("{:0.0f},{:0.0f}\n".format(i, stats[i]))

# Evalutes sudoku puzzles dataset
def evaluateSudokuDataset(puzzlesFileName, statsFileName, errorsFileName):
    import tqdm

    hasError = False
    try:
        print("Starting sudoku puzzles evaluation.")

        # Prepare the dictionary
        zeros = {}
        for i in range(0,81):
            zeros[i] = 0

        # Read the puzzles file
        with open(puzzlesFileName, "r", encoding="utf-8") as pf:
            for line in tqdm.tqdm(pf, total=getFileLineCount(puzzlesFileName)):
                # Parse the content
                data = line.split(',')
                puzzle = data[1].strip()

                # Count the number of zeros
                zeroCount = puzzle.count('0')
                zeros[zeroCount] += 1

        # Save stats
        saveStats(zeros, statsFileName)
    except Exception as e:
        hasError = True
        saveError(e, errorsFileName)

    print("Operation encountered some errors. Check {} for details or script output above.".format(errorsFileName) \
        if hasError else "Sudoku puzzles evaluator completed successfully.")
    print("Sudoku puzzles statistics saved in {}".format(statsFileName))

def main():
    import argparse

    # Register arguments
    parser = argparse.ArgumentParser();
    parser.add_argument("puzzles", help="The file name of the sudoku puzzles dataset.", type=str)
    parser.add_argument("stats", help="The file name where to save the sudoku stats.", type=str)
    parser.add_argument("errors", help="The file name where to save the errors.", type=str)

    args = parser.parse_args()

    evaluateSudokuDataset(args.puzzles, args.stats, args.errors)

if (__name__ == "__main__"):
    main()