import datasets
import mrv

def main():
	puz = datasets.sudoku_easy
	vars = mrv.select_unassigned_variable(puz)
	print("Length of vars: " + str(len(vars)))
	print("1st: " + str(vars[0]))
	print("2nd: " + str(vars[1]))
	print("Last: " + str(vars[-1]))

if __name__ == '__main__':
	main()