from sudokuBaseSolverAlg import *

def main():
    import argparse

    # Register arguments
    parser = argparse.ArgumentParser();
    parser.add_argument("puzzles", help="The file name of the sudoku puzzles dataset.", type=str)
    parser.add_argument("stats", help="The file name where to save the sudoku stats.", type=str)
    parser.add_argument("errors", help="The file name where to save the errors.", type=str)
    parser.add_argument("limit", help="The limit number of puzzles to solve.", type=int)

    args = parser.parse_args()

    solvePuzzles(args.puzzles, args.stats, args.errors, args.limit)

if (__name__=="__main__"):
    main()