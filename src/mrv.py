import solver

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

def suv(grid, arc3):
	if solver.misplaced_tiles(grid) == 0:
		return []
	else:
		ind = arc3.domain_size.flatten()
		m = min(i for i in ind if i > 1)
		index = np.where(ind==m)[0][0]
		row = index // 8
		col = index % 8
		domain = []
		for i in arc3.domain_sets[row, col, :]:
			if i > 0:
				domain.append(i)
		return [((row, col), domain)]

def select_unassigned_variable(grid):
	domains = {}
	degrees = {}
	i = 0
	while i < len(grid):
		j = 0
		while j < len(grid[i]):
			variable = (i, j)
			if (grid[i][j] == 0):
				degree_count = 0
				constraints = getConstraints(variable)
				domain = [x for x in range(1, 10)]
				for constraint in constraints:
					row, col = constraint
					val = grid[row][col]
					if val == 0:
						degree_count += 1
					elif val in domain:
						domain.remove(val)
					domains[variable] = domain
					degrees[variable] = degree_count
			j += 1
		i += 1

	result = sorted(domains.items(), key=lambda x: len(x[1]))[0]
	min_domain = len(result[1])
	minimums = [k for k in domains if len(domains[k]) == min_domain]
	degs = [(mi, degrees[mi]) for mi in minimums]
	deg_max = max(degs, key=lambda x: x[1])
	return [(deg_max[0], domains[deg_max[0]])]
