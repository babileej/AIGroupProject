#
# Class SudokuCSP is a Constraint Satisfaction Problem class specific to Sudoku puzzels
# It stores the following:
#   - puzzle, a 2D array indexed by row, col
#   - list of variable names (row, col)
#	- dictionary of domains (key = (row, col) or variable name)
#	- dictionary of binary constraints (key = (row, col) or variable name)
#
class SudokuCSP:
	boxCoords = {
		0 : [x for x in range(0, 3)],
		1 : [x for x in range(0, 3)],
		2 : [x for x in range(0, 3)],
		3 : [x for x in range(3, 6)],
		4 : [x for x in range(3, 6)],
		5 : [x for x in range(3, 6)],
		6 : [x for x in range(6, 9)],
		7 : [x for x in range(6, 9)],
		8 : [x for x in range(6, 9)]	
	}

	def __init__(self, puz):
		self.puzzle = puz
		self.variables = []
		self.domains = {}
		self.constraints = {}

	def generateBinaryConstraints(self, varName):
		constraints = []
		row_pos, col_pos = varName
		row = [(row_pos, x) for x in range(9) if x != col_pos]
		col = [(x, col_pos) for x in range(9) if x != row_pos]
		constraints += row
		constraints += col
		box_rows = self.boxCoords[row_pos]
		box_cols = self.boxCoords[col_pos]
		box = []
		for i in box_rows:
			for j in box_cols:
				if (i, j) != varName and (i, j) not in constraints:
					box.append((i,j))
		constraints += box
		self.constraints[varName] = constraints

	def buildCSP(self):
		i = 0
		while i < len(self.puzzle):
			j = 0
			while j < len(self.puzzle[i]):
				variable = (i, j)
				self.variables.append(variable)
				if (self.puzzle[i][j] > 0):
					self.domains[variable] = [self.puzzle[i][j]]
				else:
					self.domains[variable] = [x for x in range(1, 10)]
				self.generateBinaryConstraints(variable)
				j += 1
			i += 1

	def mrv(self):
		return min(filter(lambda x: len(x[1]) > 1, self.domains.items()), key=lambda x: len(x[1]))

	def pprint(self):
		for i in self.variables:
			print("Variable Name: " + str(i))
			print("Variable Domain: " + str(self.domains[i]))
			print("Variable Constraints: " + str(self.constraints[i]))
