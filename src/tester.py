import datasets
import sudokucsp

def main():
	csp = sudokucsp.SudokuCSP(datasets.sudoku_easy)
	csp.buildCSP()
	csp.pprint()
	print(csp.mrv())


if __name__ == '__main__':
  main()
