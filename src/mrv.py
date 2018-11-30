
def getConstraints(var):
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
	
	constraints = []
	
	row_pos, col_pos = var
	row = [(row_pos, x) for x in range(9) if x != col_pos]
	col = [(x, col_pos) for x in range(9) if x != row_pos]
	constraints += row
	constraints += col
	box_rows = boxCoords[row_pos]
	box_cols = boxCoords[col_pos]
	box = []
	for i in box_rows:
		for j in box_cols:
			if (i, j) != var and (i, j) not in constraints:
				box.append((i,j))
	constraints += box
	
	return constraints

def select_unassigned_variable(grid):
	domains = {}
	
	i = 0
	while i < len(grid):
		j = 0
		while j < len(grid[i]):
			variable = (i, j)
			if (grid[i][j] > 0):
				domains[variable] = [grid[i][j]]
			else:
				constraints = getConstraints(variable)
				domain = [x for x in range(1, 10)]
				for constraint in constraints:
					row, col = constraint
					if grid[row][col] in domain:
						domain.remove(grid[row][col])
					domains[variable] = domain
				
			j += 1
		i += 1
		
	return sorted(filter(lambda x: len(x[1]) > 1, domains.items()), key=lambda x: len(x[1])) 

