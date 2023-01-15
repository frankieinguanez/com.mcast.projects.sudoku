import sudokuSolverAlg as solver
import sudokuPuzzleUtils as spu

def solvePuzzles(puzzlesFileName, statsFileName, errorsFileName, limit, searchMode, guessMode):
    """
    Solves puzzles found in a file using backtracking algorithm.
    Arguments:
        puzzlesFileName: file containing puzzles in following format: <id>, <puzzle>, <solution>
        statsFileName: file where statistics shall be saved.
        errorsFileName: file where errors shall be saved.
        limit: the limit number of puzzles to solve.
        searchMode: defines how missing values are searched.
        guessMode: defines how guesses are made.
    """
    import tqdm

    if not limit:
        limit = spu.getFileLineCount(puzzlesFileName)

    i = 1
    hasError = False
    try:
        print("Starting sudoku base solver.")
        
        with open(statsFileName, "w", encoding="utf-8") as sf:
            with open(puzzlesFileName, "r", encoding="utf-8") as pf:
                for line in tqdm.tqdm(pf, total=limit):
                    # Stop at limit
                    if (i>limit):
                        break
                    
                    # Parse the content
                    data = line.split(',')
                    p = data[1].strip()

                    # Create board and statistics
                    board = spu.to2DArray(p)
                    stats = spu.SudokuStats();

                    # Start statistics gathering and solve
                    stats.registerStartTime()
                    solver.backtracking(board, stats, searchMode, guessMode)
                    stats.registerEndTime()
                        
                    # Write statistics
                    sf.write("{},{},{:0.22f},{:0.0f},{:0.0f}\n".format(p, spu.toStr(board), stats.executionTime(), stats.guesses, stats.backtracks))
                    i+=1

    except Exception as e:
        hasError = True
        spu.saveError(e, errorsFileName)

    print("Operation encountered some errors. Check {} for details or script output above.".format(errorsFileName) \
        if hasError else "Sudoku puzzles solved completed successfully.")
    print("Sudoku solver statistics saved in {}".format(statsFileName))

def main():
    import argparse

    # Register arguments
    parser = argparse.ArgumentParser();
    parser.add_argument("puzzles", help="The file name of the sudoku puzzles dataset.", type=str)
    parser.add_argument("stats", help="The file name where to save the sudoku stats.", type=str)
    parser.add_argument("errors", help="The file name where to save the errors.", type=str)
    parser.add_argument("limit", help="The limit number of puzzles to solve.", type=int)
    parser.add_argument("search", help="Defines how the puzzle is parsed: 1 by row; 2 by col; 3 by box sequentially; 4 by box in a zig-zag; 5 by box in a spiral; 6 by box in a semi-zig-zag.", type=int)
    parser.add_argument("guess", help="defines how numbers are guessed: 1 sequentially; 2 randomly.", type=int)

    args = parser.parse_args()

    solvePuzzles(args.puzzles, args.stats, args.errors, args.limit, args.search, args.guess)

if (__name__=="__main__"):
    main()